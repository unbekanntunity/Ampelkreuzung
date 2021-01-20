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

class Warteschlange(object):

    def __init__(self):
        self.schlange = []
        self.warteschlangename = []

    def anhaengen(self, laenge):
        self.schlange.append(laenge)

    def hinzufuegen(self, index):
        self.schlange.insert(index)

    def loeschen(self, index):
        self.schlange.pop(index)

    def getlen(self):
        return len(self.schlange)
