#-------------------------------------------------------------------------------
# Name:        Timer
# Purpose:     Zeituhr
# Author:      T.nguyen, T. Rothe 
# Created:     13.01.2021
# Modified:    13.01.2021
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time as t
import threading as thread
import Warteschlange

class Stoppuhr(thread.Thread):

    """
    Eine Klasse für die Simulation einer Timer. 
    Solange der Thread nicht mit der finish()-funktion geschlossen wird, läuft der Thread in einer Schleife weiter.
    Dort wiederholt sie folgende Schritte:
        - Erst wartet der Thread für eine gewissen Intervall
        - Dann wird die Zeit die gewartet wurde, zu die Variable `value`dazuaddiert
    """

    def __init__(self, intervall = 0.001):
        thread.Thread.__init__(self)
        self.intervall = intervall
        self.pruefintervall = 1 
        self.value = 0
        self.ampelkreuzung = None
        self.alive = False

    #Wird jeden Fram aufgreufen bis der Thread mit obj.finish() beendet wird
    def run(self):
        self.alive = True   
        self.letzterWert = self.value
        while self.alive:
            t.sleep(self.intervall)
            self.value += self.intervall
            if(self.value - self.letzterWert >= self.pruefintervall):
                if(self.ampelkreuzung != None):
                    self.ampelkreuzung.autoanstellen()            
                self.letzterWert = self.value

    #Beendet die Stopuhr, bei Methodenaufruf
    def finish(self):
        self.alive = False
        return self.value

    #Setzt den Wert der Stoppuhr zurück
    def zuruecksetzen(self):
        self.value = 0
    
    #Gibt die aktuelle Zeit zurück
    def zeit(self):
        return self.value