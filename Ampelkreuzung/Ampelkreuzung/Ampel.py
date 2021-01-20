#-------------------------------------------------------------------------------
# Name:        Ampel
# Purpose:     Allgemeines Objekt für eine Ampel
#
# Author:      T.nguyen, T. Rothe 
#
# Created:     13.01.2020
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Timer 

import threading as thread

class Ampel(thread.Thread):

    def __init__ (self):
        thread.Thread.__init__(self)
        self.timer = Timer.Stoppuhr(1)
        self.alive = False
        self.zustand = False    
        self.rotphasenlaenge = []
        self.gruenphasenlaenge = []
        self.ampelname = ""
        self.index = 0

    def umschalten(self):
        if(self.zustand):
            self.zustand = False
            self.timer.zuruecksetzen()
        else:
            self.zustand = True
            self.timer.zuruecksetzen()
    
    def run(self):
        self.alive = True
        self.timer.start()
        while(self.alive):
            if(self.zustand == True and self.timer.zeit() >= self.gruenphasenlaenge[0]):
                self.umschalten()
            elif(self.zustand == False and self.timer.zeit() >= self.rotphasenlaenge[0]):
                self.umschalten()

    def finish(self):
        self.alive = False
        self.timer.finish()