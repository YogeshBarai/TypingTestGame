import math
import time

class TypingTestCalculations:

    def get_mismatch_index(self, typedtext, orgtext):
        if len(typedtext) ==0:
            return 0
        for i in range(min(len(typedtext), len(orgtext))):
            if typedtext[i] != orgtext[i]:
                return i
        return min(len(typedtext), len(orgtext))

    def get_elapsed_time(self, starttime):
        return time.time() - starttime

    def get_speed(self, wordslist, starttime):
        return "{0:.2f}".format(60 * len(wordslist / self.get_elapsed_time(starttime)))

    def get_required_lines(self, orgtext, terminalwidth):
        return int(math.ceil(len(orgtext) / terminalwidth))
