#-------------------------------------------------------------------------------
# Name:        Warteschlange
# Purpose:     Allgemeines Objekt für eine Wartscheschlange
#
# Author:      T.nguyen, T. Rothe 
#
# Created:     09.12.2020
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time as t
import Timer 
import threading 
class Warteschlange(object):

    def __init__(self):
        self.schlange = []
        self.warteschlangename = ""
        self.inprozess = False
        self.abgearbeitetautos = 0
        
    def anhaengen(self, laenge):
        self.schlange.append(laenge)

    def abarbeitenstarten(self):
        if(self.inprozess == False):
            self.inprozess = True
            threading._start_new_thread(self.abarbeiten)

    def hinzufuegen(self, index):
        self.schlange.insert(index)

    def loeschen(self, index):
        self.schlange.pop(index)

    def getlen(self):
        return len(self.schlange)

    def abarbeiten(self):
        if(len(self.schlange) > 0):
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAA")
            t.sleep(self.schlange[0])
            self.schlange.pop(0)
            self.abgearbeitetautos += 1
        self.inprozess = False