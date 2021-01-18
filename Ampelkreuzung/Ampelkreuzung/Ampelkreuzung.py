#-------------------------------------------------------------------------------
# Name: Ampelkreuzung
# Purpose: Simulation einer Ampel
#
# Author: T.nguyen, T.  Rothe
#
# Created: 13.01.2020
# Copyright: (c) an.nguyen 2020
# Licence: <your licence>
#-------------------------------------------------------------------------------

import Ampel 
import Warteschlange 
import random
import Timer

class Ampelkreuzung(object):

    def __init__(self):
        self.anstellWahrscheinlichkeit = 0.5
        self.maxdurchlaufe = 10
        self.anzahlWarteschlangen = 8
        self.anzahlAmpeln = 8

        self.gruenphasenlaenge = [5 , 3 , 5 , 3]
        self.rotphasenlaenge = []
        self.warteschlangen = []
        self.ampeln = []

        self.stoppuhr = Timer.Stoppuhr(1)
        self.stoppuhr.ampelkreuzung = self
        self.nummer = 0
        
        for self.warteschlangeIndex in range(self.anzahlWarteschlangen):
            self.warteschlange = Warteschlange.Warteschlange()
            self.warteschlangen.append(self.warteschlange)

        for ampelIndex in range(self.anzahlAmpeln):
            ampel = Ampel.Ampel()
            if len(self.gruenphasenlaenge) > 1:
                for i in range(len(self.gruenphasenlaenge)):
                    if ampelIndex < 4 and i % 2 == 0:
                        ampel.gruenphaselaenge.append(self.gruenphasenlaenge[i])
                    elif ampelIndex >= 4 and i % 1 == 1:
                        ampel.gruenphaselaenge.append(self.gruenphasenlaenge[i])

                    try:
                        ampel.rotphaselaenge.append(self.gruenphasenlaenge[i + 1])
                    except:
                        ampel.rotphaselaenge.append(self.gruenphasenlaenge[i - 1])
            else:
                ampel.gruenphaselaenge = self.gruenphasenlaenge[0]
                ampel.rotphaselaenge = self.gruenphasenlaenge[0]
            self.ampeln.append(ampel)

        self.stoppuhr.start()
        
        done = False

        while(done == False):
            eingabe = input("Um zu beenden einfach eine Taste drücken")
            if eingabe == "":
                done = True

        print(self.stoppuhr.zeit())
        self.stoppuhr.finish()
        
    def Autoanstellen(self):
        for warteschlange in self.warteschlangen:
            self.nummer = random.random()
            print(self.nummer)
            if self.nummer <= self.anstellWahrscheinlichkeit:
                warteschlange.anhaengen(2)
                print(f"{warteschlange.schlange[0]} || {self.nummer}")
            

ampelkreuzungstart = Ampelkreuzung()