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

class Ampel(object):

    def __init__ (self):
        self.zustand = False    
        self.timer = Timer.Stoppuhr(1)
        self.rotphaselaenge = []
        self.gruenphaselaenge = []
        self.index = 0

    def umschalten(self):
        if(self.zusatnd):
            self.zusatnd = False
            self.timer.reset()
        else:
            self.zusatnd = True
            self.timer.reset()
    
    