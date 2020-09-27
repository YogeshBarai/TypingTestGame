import pygame
from pygame.locals import *
import os
import sys
import time
from datetime import datetime, timedelta
#import signal
#import TypingTestCalculations
#import TypingTestCmd
import TypingTestDB
#import KeyPress
import random

class TypingTestAppV2:
    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = True
        self.USER_SENT = ''
        self.ORG_SENT = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)
        self.RESET_C = (250, 250, 250)

        self.db = TypingTestDB.TypingTestDB()
        self.randomTextId = random.randint(1,5000)
        self.dbtext = self.db.search(self.randomTextId)
        
        pygame.init()
        self.RESULT_FONT = pygame.font.SysFont("Verdana", 20)
        self.RESULT_POS = (0, self.h/1.5 - 50)
        self.HEADER_FONT = pygame.font.SysFont("Verdana", 20)
        self.HEADER_POS = (self.w/4, 0)
        self.ORG_SENT_FONT = pygame.font.SysFont("Verdana", 20)
        self.ORG_SENT_POS = (0,50)
        self.USER_SENT_FONT = pygame.font.SysFont("Verdana", 20)
        self.USER_SENT_POS = (0,round(self.h/1.5))
        self.RESET_FONT = pygame.font.SysFont("Verdana", 20)
        self.RESET_POS = (self.w/2, self.h)
        self.curr_file_path = os.path.dirname(os.path.abspath(__file__))
        print('/n')
        self.curr_file_path = self.curr_file_path[:self.curr_file_path.rfind('\\')]
        img_file_path = self.curr_file_path + r'\TypingTestGame\images\background.jpg'
        print(img_file_path)
        self.open_img = pygame.image.load(img_file_path)
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))
        self.bg = pygame.image.load(img_file_path)
        self.bg = pygame.transform.scale(self.bg, (750, 500))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Typing Test Game')

    def draw_text(self, screen, text, pos, color, fontobj):
        #font = pygame.font.Font(None, fsize)
        font = fontobj
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = screen.get_size()
        x, y = pos

        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        #text = font.render(text, 1, color)
        #text_rect = text.get_rect(center=(self.w/2, y))
        #screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        self.randomTextId = random.randint(1,5000)
        self.dbtext = self.db.search(self.randomTextId)
        sentence = self.dbtext
        return sentence

    def show_results(self, screen):
        if(not self.end):

            #Calculate time
            self.total_time = time.time() - self.time_start

            #Calculate accuracy
            count = 0
            for i, c in enumerate(self.ORG_SENT):
                try:
                    if self.USER_SENT[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.ORG_SENT)*100

            #Calculate words per minute
            self.wpm = len(self.USER_SENT)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time:'+str(round(self.total_time)) + " secs   Accuracy:" + str(
                round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # draw icon image
            self.time_img = pygame.image.load(self.curr_file_path + r'\TypingTestGame\images\icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))

            #screen.blit(self.time_img, (80,320))
            #screen.blit(self.time_img, (self.w/2-75, self.h-140))
            self.draw_text(screen, "Reset", self.RESET_POS, self.RESET_C, self.RESET_FONT)

            print(self.results)
            pygame.display.update()

    def run(self):
        print("Inside Run...")
        self.reset_game()

        self.running = True
        while(self.running):
            clock = pygame.time.Clock()
            #self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            #pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)

            # update the text of user input
            #if self.input_text != '':
            self.screen.fill((0, 0, 0), (0, round(self.h/1.5), self.w, self.h))
            self.draw_text(self.screen, self.USER_SENT, self.USER_SENT_POS, self.TEXT_C, self.USER_SENT_FONT)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if(x >= 0 and x <= round(self.h/1.5) and y >= self.w and y <= self.h):
                        print("Inside box...")
                        self.active = True
                        self.USER_SENT = ''
                        self.time_start = time.time()
                     # position of reset box
                    if(x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            self.USER_SENT = ''
                            self.end = True
                            self.running = False
                            self.active = False
                            sys.exit()
                    elif self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.USER_SENT)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, self.RESULT_POS, self.RESULT_C, self.RESULT_FONT)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.USER_SENT = self.USER_SENT[:-1]
                            pygame.display.update()
                        else:
                            if len(self.USER_SENT) == 1:
                                self.active = True
                                self.time_start = time.time()
                            try:
                                self.USER_SENT += event.unicode
                                pygame.display.update()
                            except:
                                pass
            
            pygame.display.update()

        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)
        self.reset = False
        self.end = False
        self.USER_SENT = ''
        self.ORG_SENT = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence
        self.ORG_SENT = self.get_sentence()
        if (not self.ORG_SENT):
            self.reset_game()

        #drawing heading
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        headerText = "Typing Test -  Improve your typing skills."
        self.draw_text(self.screen, headerText, self.HEADER_POS, self.HEAD_C, self.HEADER_FONT)

        # draw the rectangle for input box
        #pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.ORG_SENT, self.ORG_SENT_POS, self.TEXT_C, self.ORG_SENT_FONT)

        pygame.display.update()