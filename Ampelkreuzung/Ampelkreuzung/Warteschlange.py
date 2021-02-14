#-------------------------------------------------------------------------------
# Name:        Warteschlange
# Purpose:     Allgemeines Objekt für eine Wartscheschlange
# Author:      T.nguyen, T. Rothe 
# Created:     09.12.2020
# Modified:    13.01.2021
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time as t
import Timer 
import threading 


class Warteschlange(object):
    """
    Sind die Schlangen in denen die Autos anstehen.
    Jede Spur hat eine eigene Schlange.
    Das Abarbeiten geschieht mit Hilfe von Thread, da wir mit der Sleepfunktion arbeiten und sonst das Hauptprogramm beeinträchtigt wird.
    Erst wenn der Thread fertig ist und das Element entfernt wurde, kann das nächste Element abgearbeitet werden.
    """

    def __init__(self):
        self.warteschlangename = ""
        self.schlange = []
        self.inprozess = False
        self.abgearbeitetautos = 0
        self.anstellwahrscheinlichkeit = 0.5

    #Hängt ein übergebenes Element in die Liste an
    def anhaengen(self, element):
        self.schlange.append(element)

    #Ermöglicht das Abarbeiten als Hintergrundaktion
    def abarbeitenstarten(self):
        if(self.inprozess == False):
            self.inprozess = True
            threading._start_new_thread(self.abarbeiten)

    #Entfernt das erste Element(autos) aus der Warteschlange
    def abarbeiten(self):
        if(len(self.schlange) > 0):     #Geht nur wenn elemente in schlange sind
            t.sleep(self.schlange[0])   #Nimmt das erste Elemnt als Zeit, die er wartet
            self.schlange.pop(0)        #Entfernt das erste Element der Warteschlange
            self.abgearbeitetautos += 1 
        self.inprozess = False          