#-------------------------------------------------------------------------------
# Name: Ampelkreuzung
# Purpose: Simulation einer Ampel
#
# Author: T.nguyen, T. Rothe 
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

        self.zeitProAuto = 2
        self.anstellWahrscheinlichkeit = 0.5
        self.maxdurchlaufe = 10

        self.gruenphasenlaenge = []
        self.rotphasenlaenge = []
        self.warteschlangen = []
        self.ampeln = []
        self.ampelnamen = ["AmpelA11(mitte)", "AmpelA21(mitte)", "AmpelA12(links)", "AmpelA21(links)", "AmpelB11(mitte)", "AmpelB21(mitte)", "AmpelB12(links)", "AmpelB21(links)"]
        self.warteschlangennamen = ["WarteschlangeA11(mitte)", "WarteschlangeA21(mitte)", "WarteschlangeA12(links)", "WarteschlangeA21(links)", "WarteschlangeB11(mitte)", "WarteschlangeB21(mitte)", "WarteschlangeB12(links)", "WarteschlangeB21(links)"]

        self.stoppuhr = Timer.Stoppuhr(1)
        self.stoppuhr.ampelkreuzung = self
        self.nummer = 0
        self.eingabe = ""
        self.done = False

        # Erstellen der Objekten
        for warteschlangeIndex in range(8):
            warteschlange = Warteschlange.Warteschlange()
            warteschlange.warteschlangename = self.warteschlangennamen[warteschlangeIndex]
            self.warteschlangen.append(warteschlange)

        for ampelIndex in range(8):
            ampel = Ampel.Ampel()
            ampel.ampelname = self.ampelnamen[ampelIndex]
            self.ampeln.append(ampel)
        
        #Eingabe für die Grünüphasenlängen
        for i in range(4):
            self.gruenphasenlaenge.append(int(input(f"Ampel: {i}" + "\n")))

        anstellWahrscheinlichkeit = int(input(f"Wahrscheinlichkeit der Autos: \n"))
        zeitProAuto = int(input("Durchschnittliche Dauer pro Auto:"))

        for index in range(len(self.ampeln)):
            self.ampeln[index].gruenphasenlaenge.clear()
            self.ampeln[index].rotphasenlaenge.clear()

        # Grünphasenkalkulation
        for index in range(len(self.gruenphasenlaenge)):
            self.ampeln[index * 2].gruenphasenlaenge.append(self.gruenphasenlaenge[index])
            self.ampeln[(index * 2) + 1].gruenphasenlaenge.append(self.gruenphasenlaenge[index])

        #Rotphasenkalkulation
        if len(self.gruenphasenlaenge) > 1:
            self.ampeln[0].rotphasenlaenge.append(((self.ampeln[2].gruenphasenlaenge[0]) - (self.ampeln[0].gruenphasenlaenge[0] - (self.ampeln[0].gruenphasenlaenge[0] * 0.8))) + ((self.ampeln[6].gruenphasenlaenge[0]) - (self.ampeln[4].gruenphasenlaenge[0] - (self.ampeln[4].gruenphasenlaenge[0] * 0.8)) + self.ampeln[4].gruenphasenlaenge[0]))           
            self.ampeln[1].rotphasenlaenge.append(self.ampeln[0].rotphasenlaenge[0])

            self.ampeln[2].rotphasenlaenge.append(0.8 * self.ampeln[0].gruenphasenlaenge[0] + (0.8 * self.ampeln[4].gruenphasenlaenge[0] + self.ampeln[6].gruenphasenlaenge[0])) 
            self.ampeln[3].rotphasenlaenge.append(self.ampeln[2].rotphasenlaenge[0])

            self.ampeln[4].rotphasenlaenge.append(((self.ampeln[6].gruenphasenlaenge[0]) - (self.ampeln[4].gruenphasenlaenge[0] - (self.ampeln[4].gruenphasenlaenge[0] * 0.8))) + ((self.ampeln[2].gruenphasenlaenge[0]) - (self.ampeln[0].gruenphasenlaenge[0] - (self.ampeln[0].gruenphasenlaenge[0] * 0.8)) + self.ampeln[0].gruenphasenlaenge[0]))
            self.ampeln[5].rotphasenlaenge.append(self.ampeln[4].rotphasenlaenge[0])

            self.ampeln[6].rotphasenlaenge.append(0.8 * self.ampeln[4].gruenphasenlaenge[0] + (0.8 * self.ampeln[0].gruenphasenlaenge[0] + self.ampeln[2].gruenphasenlaenge[0])) 
            self.ampeln[7].rotphasenlaenge.append(self.ampeln[6].rotphasenlaenge[0])

        for index in range(len(self.ampeln)):
            print(f"{self.ampeln[index].ampelname}: {self.ampeln[index].gruenphasenlaenge[0]}")
            print(f"{self.ampeln[index].ampelname}: {self.ampeln[index].rotphasenlaenge[0]}")
        print("")
        
        self.starten()

    def starten(self):
        self.stoppuhr.start()
        for ampelIndex in range(len(self.ampeln)):
            self.ampeln[ampelIndex].start()
        
        while(self.done == False):
            if(self.eingabe == "e"):
                print("done")
                self.done = True
                print(self.stoppuhr.zeit())
                self.stoppuhr.finish()
                for ampelIndex in range(len(self.ampeln)):
                    self.ampeln[ampelIndex].finish()

    def Autoanstellen(self):
        for warteschlange in self.warteschlangen:
            self.nummer = random.random()
            if self.nummer <= self.anstellWahrscheinlichkeit:
                warteschlange.anhaengen(self.zeitProAuto)
            
    def Ausgabe(self):
        for ampelIndex in range(len(self.ampeln)):
            print(f"{self.ampeln[ampelIndex].ampelname}:  {self.ampeln[ampelIndex].zustand}")
            print(f"{self.warteschlangen[ampelIndex].warteschlangename}:  {self.warteschlangen[ampelIndex].schlange} \n")

        self.eingabe = input("\n weitermachen = enter drücken, beenden = `e` eingeben \n")
      
ampelkreuzungstart = Ampelkreuzung()