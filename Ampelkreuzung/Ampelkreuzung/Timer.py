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
import Warteschlange

class Stoppuhr(thread.Thread):

    def __init__(self, intervall = 0.001):
        thread.Thread.__init__(self)
        self.intervall = intervall
        self.ampelkreuzung = None
        self.value = 0
        self.alive = False

    def run(self):
        self.alive = True
        while self.alive:
            t.sleep(self.intervall)
            self.value += self.intervall
            self.ampelkreuzung.Autoanstellen()
            

    def finish(self):
        self.alive = False
        return self.value

    def zuruecksetzen(self):
        self.value = 0

    def zeit(self):
        return self.value