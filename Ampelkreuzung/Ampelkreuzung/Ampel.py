#-------------------------------------------------------------------------------
# Name:        Ampel
# Purpose:     Allgemeines Objekt für eine Ampel
# Author:      T.nguyen, T. Rothe 
# Created:     13.01.2021
# Modified:    26.01.2021
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Timer 

import threading as thread

class Ampel(thread.Thread):
    """
    Diese Klasse ist für die Simulation einer Ampel da. 
    Sie besitzt zwei Listen , die für die jeweiligen Längen der Phasen verantwortlicht sind. 
    Der Index ist für beide Listen da und repräsentiret die momentanen Phase.
    Zudem hat diese einen eigenen Timer, der im Hintergrund läuft und zurückgesetzt wird, wenn diese Ampel umschaltet, also die Variable `Zustand` ändert.
    Die Variable `Zustand` steht ´für die momentane Farbe der Ampel. 
        False steht für Rot 
        True steht für Grün
    Gelb haben wir ausgelassen, da man dies in die Grünphase mit einbeziehen kann, da die Autos dort meistens immernoch über die Straße fahren.
    """

    def __init__ (self):
        #Besitzt jeweils einen eigenen unabhängigen Timer, der für den Wechsel der Rot-Grünphasen verantwortlich ist
        thread.Thread.__init__(self)
        self.timer = Timer.Stoppuhr(1)
        self.alive = False
        self.zustand = "Rot"              
        self.rotphasenlaenge = []
        self.gruenphasenlaenge = []
        self.ampelname = ""
        self.index = 0

    #Schaltet die Ampel um
    def umschalten(self):                 #von grün nach rot (grün = true)
        if(self.zustand == "Grün"):
            self.indexerhoehen()
            self.zustand = "Rot"          #Timer wird zurückgesetzt
            self.timer.zuruecksetzen()    #von rot nach grün
        else:                      
            self.indexerhoehen()
            self.zustand = "Grün"
            self.timer.zuruecksetzen()
     
    #Diese Funktion kommt mit dem Import des Threadmodules und wird solange ausgelöst bis der Thread geschlossen wird
    def run(self):                
        self.alive = True
        self.timer.start()
        #Schleife, die die vergangende Zeit, den Index der Grünphasenlänge und den momentenen Zustand überprüft
        while(self.alive):                
            if(self.zustand == "Grün" and self.timer.zeit() >= self.gruenphasenlaenge[self.index]):   
                self.umschalten()
            elif(self.zustand == "Rot" and self.timer.zeit() >= self.rotphasenlaenge[self.index]):  
                self.umschalten()

    #Da wir eine Liste mit verschiedenen Grünphasenlängen haben, brauchen wir auch ein Index
    def indexerhoehen(self):
        if(self.index < (len(self.gruenphasenlaenge) - 1)):
            self.index += 1
        else:
            self.index = 1

    #Beendet den Thread sobald diese Methode aufgreufen wird(Kommt ebenfalls mit den Import des Threadmodule)
    def finish(self):
        self.alive = False
        self.timer.finish()