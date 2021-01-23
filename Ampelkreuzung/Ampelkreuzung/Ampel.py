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
            self.indexerhoehen()
            self.zustand = False
            self.timer.zuruecksetzen()
        else:
            self.indexerhoehen()
            self.zustand = True
            self.timer.zuruecksetzen()
    
    def run(self):
        self.alive = True
        self.timer.start()
        while(self.alive):
            if(self.zustand == True and self.timer.zeit() >= self.gruenphasenlaenge[self.index]):
                self.umschalten()
            elif(self.zustand == False and self.timer.zeit() >= self.rotphasenlaenge[self.index]):
                self.umschalten()

    def indexerhoehen(self):
        if(self.index < (len(self.gruenphasenlaenge) - 1)):
            self.index += 1
        else:
            self.index = 1

    def finish(self):
        self.alive = False
        self.timer.finish()