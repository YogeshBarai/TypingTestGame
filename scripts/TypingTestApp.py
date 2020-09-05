import curses
import os
import sys
import time
from datetime import datetime, timedelta
import signal
from TypingTestCalculations import TypingTestCalculations
from TypingTestCmd import TypingTestCmd
import KeyPress

class typing_test_app:
    def __init__(self):
        Cmd = TypingTestCmd()
        Calc = TypingTestCalculations()

        self.text = Cmd.get_text()
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
        curses.wrapper(self.main)

    def main(self, windowObj):
        
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



        
