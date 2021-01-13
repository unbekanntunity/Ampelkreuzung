#-------------------------------------------------------------------------------
# Name:        Timer
# Purpose:     Zeituhr
#
# Author:      T.nguyen, T. Rothe 
#
# Created:     13.01.2020
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time as t
import threading as thread

class Timer(thread.Thread):

    def __init__(self, interval=0.001):
        thread.Thread.__init__(self)
        self.interval = interval  
        self.value = 0
        self.alive = False

    def run(self):
        self.alive = True
        while self.alive:
            t.sleep(self.interval)
            self.value += self.interval

    def reset(self):
        self.value = 0

    def peek(self):
        return self.value

    def finish(self):
        self.alive = False
        return self.value

