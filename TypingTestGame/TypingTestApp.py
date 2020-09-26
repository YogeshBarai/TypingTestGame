import os
import sys
import time
from datetime import datetime, timedelta
import signal
import TypingTestCalculations
import TypingTestCmd
import KeyPress
from curses import wrapper
import curses

class TypingTestApp:
    def __init__(self):
        self.Cmd = TypingTestCmd.TypingTestCmd()
        self.Calc = TypingTestCalculations.TypingTestCalculations()
        
        self.text = self.Cmd.get_text()
        self.words = self.text.split()
        self.text = " ".join(self.words)
        self.orgtext = self.text

        self.currentWord = ""
        self.currentString = ""

        self.key = ""
        self.testStart = False
        self.userKeyStrokes = []

        self.startTime = 0
        self.endTime = 0
        self.i = 0
        self.mode = 0
        self.terminalHeight = 0
        self.terminalWidth = 0
        self.lineCount = 0
        self.wpm = 0
        sys.stdout = sys.__stdout__
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        
        curses.wrapper(self.main)
        
    def main(self, windowObj):
        self.initialize(windowObj)

        def signalHandler(sig, frame):
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signalHandler)

        while True:
            key = self.keyinput(windowObj)

            if KeyPress.is_escape(key):
                sys.exit(0)
            if self.mode == 0:
                self.start_typing_test(windowObj, key)
            elif self.mode == 1 and KeyPress.is_enter(key):
                self.replay(windowObj)
            windowObj.refresh()

    
    def initialize(self, winObj):
        self.terminalHeight, self.terminalWidth = self.getTerminalDimensions(winObj)
        self.text = self.word_wrap(self.text, self.terminalWidth)

        self.lineCount = self.Calc.get_required_lines(self.text, self.terminalWidth) + 3

        if self.lineCount > self.terminalWidth:
            self.sizeError()

        winObj.nodelay(False)
        self.setPrint(winObj)

    def word_wrap(self, text, width):
        for x in range(1, self.Calc.get_required_lines(text, width) + 1):
            if not (x * width >= len(text) or text[x * width - 1] == " "):
                i = x * width - 1
                while text[i] != " ":
                    i -= 1
                text = text[:i] + " " * (x * width - i) + text[i + 1 :]
        return text

    def getTerminalDimensions(self, winObj):
        return winObj.getmaxyx()
    
    def setPrint(self, winObj):
        with open("TypingTestGame\GameOptions.md", encoding="utf-8") as f:
            GAME_OPTIONS = f.read()
        winObj.addstr(0, int(self.terminalWidth / 2) - 4, " TypingTest ", curses.color_pair(3))
        winObj.addstr(1, 0, GAME_OPTIONS , curses.color_pair(3))
        winObj.addstr(6, 0, self.text, curses.A_BOLD)

    def start_typing_test(self, win, key):
        if not self.testStart and KeyPress.is_valid_initial_key(key):
            self.startTime = time.time()
            self.testStart = True
        if KeyPress.is_resize(key):
            self.resize(win)
        if not self.testStart:
            return
        self.userKeyStrokes.append([time.time(), key])
        self.key_printer(win, key)

    def key_printer(self, win, key):
        # Exit on escape
        if KeyPress.is_escape(key):
            sys.exit(0)

        # Handle resizing
        elif KeyPress.is_resize(key):
            self.resize(win)

        # Check for backspace
        elif KeyPress.is_backspace(key):
            self.erase_key()

        # Check for space
        elif key == " ":
            self.check_word()

        # Check for any other typable characters
        elif KeyPress.is_valid_initial_key(key):
            self.appendkey(key)

        # Update state of window
        self.update_state(win)

    def keyinput(self, win):
        key = ""
        while key == "":
            try:
                if sys.version_info[0] < 3:
                    key = win.getkey()
                    return key

                key = win.get_wch()
                if isinstance(key, int):
                    if key in (curses.KEY_BACKSPACE, curses.KEY_DC):
                        return "KEY_BACKSPACE"
                    if key == curses.KEY_RESIZE:
                        return "KEY_RESIZE"
            except curses.error:
                continue
        return key

    def erase_key(self):
        if len(self.currentWord) > 0:
            self.currentWord = self.currentWord[0 : len(self.currentWord) - 1]
            self.currentString = self.currentString[0 : len(self.currentString) - 1]

    def check_word(self):
        spc = self.Calc.get_space_count(len(self.currentString), self.text)
        if self.currentWord == self.words[self.i]:
            self.i += 1
            self.currentWord = ""
            self.currentString += spc * " "
        else:
            self.currentWord += " "
            self.currentString += " "

    def appendkey(self, key):
        self.currentWord += key
        self.currentString += key

    def update_state(self, win):
        win.addstr(self.lineCount, 0, " " * self.terminalWidth)
        win.addstr(self.lineCount, 0, self.currentWord)

        win.addstr(2, 0, self.text, curses.A_BOLD)
        win.addstr(2, 0, self.text[0 : len(self.currentString)], curses.A_DIM)

        index = self.Calc.get_mismatch_index(self.currentString, self.text)
        win.addstr(
            2 + index // self.terminalWidth,
            index % self.terminalWidth,
            self.text[index : len(self.currentString)],
            curses.color_pair(2),
        )

        if index == len(self.text):
            win.addstr(self.lineCount, 0, " Your typing speed is ")
            if self.mode == 0:
                self.wpm = self.Calc.get_speed(
                    self.words, self.startTime
                )

            win.addstr(" " + self.wpm + " ", curses.color_pair(1))
            win.addstr(" WPM ")

            win.addstr(self.lineCount + 2, 0, " Press ")

            win.addstr(" Enter ", curses.color_pair(6))

            win.addstr(" to see a replay! ")

            if self.mode == 0:
                self.mode = 1
                for k in range(len(self.userKeyStrokes) - 1, 0, -1):
                    self.userKeyStrokes[k][0] -= self.userKeyStrokes[k - 1][0]
            self.userKeyStrokes[0][0] = 0
            self.testStart = False
            self.endTime = time.time()
            self.currentString = ""
            self.currentWord = ""
            self.i = 0

            self.startTime = 0
        win.refresh()

    def replay(self, win):

        win.addstr(self.lineCount + 2, 0, " " * self.terminalWidth)

        self.setPrint(win)

        for j in self.userKeyStrokes:
            time.sleep(j[0])

            self.key_printer(win, j[1])

    def resize(self, win):
        win.clear()
        self.terminalHeight, self.terminalWidth = self.getTerminalDimensions(win)
        self.text = self.word_wrap(self.orgtext, self.terminalWidth)
        self.lineCount = (
            self.Calc.get_required_lines(self.text, self.terminalWidth) + 2 + 1
        )
        self.setPrint(win)

        self.update_state(win)

        win.refresh()

    def sizeError(self):
        sys.stdout.write("Window too small to print given text")
        curses.endwin()
        sys.exit(-1)