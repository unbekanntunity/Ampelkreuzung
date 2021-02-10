#-------------------------------------------------------------------------------
# Name:        Ampelkreuzung
# Purpose:     Simulation einer Ampelkreuuzung
#
# Author:      T.nguyen, T. Rothe 
# Created:     13.01.2021
# Modified:    26.01.2021
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Ampel 
import Warteschlange 
import random
import Timer
import pickle

class Ampelkreuzung(object):
    """
    Diese Klasse ist für die Simulation da und bezieht jede einzelklasse(Ampel, Warteschlange und Timer) mit ein.
    Sie besitzt neben den Simulationsprozess auch ein kleines Interface.
    """

    def __init__(self):
        self.sekundenProAuto = 2
        self.maxdurchlaufe = 5
        self.verzoegerung = 0.8
        self.ausgabegeschwindigkeit = 0.5

        self.anstellwahrscheinlichkeit =[0.5]
        self.gruenphasenlaenge = [3]
        self.rotphasenlaenge = []
        self.warteschlangen = []
        self.einstellungenOptionen =  []
        self.ampeln = []
        self.ampelnamen = ["AmpelA11(mitte)", "AmpelA21(mitte)", "AmpelA12(links)", "AmpelA21(links)", "AmpelB11(mitte)", "AmpelB21(mitte)", "AmpelB12(links)", "AmpelB21(links)"]
        self.warteschlangennamen = ["A11(mitte)", "A21(mitte)", "A12(links)", "A21(links)", "B11(mitte)", "B21(mitte)", "B12(links)", "B22(links)"]
        self.optionen = [["Simulation starten", lambda: self.starten()],["Einstellungen", lambda: self.einstellungen()], ["Programm beenden", lambda: self.programmBeenden()]]

        self.nummer = 0
        self.durchlaeufe = -1
        self.indexletztezahl = 0
        self.gruenphasendurchlauefe = 0
        self.eingabe = ""
        self.pruefinterall = 1
        self.datenVorhanden = False
        self.fertig = False
        self.eingabeBeendet = False
        self.standarteinstellungen = True

        self.stoppuhr = Timer.Stoppuhr(1)
        self.stoppuhr.ampelkreuzung = self
        self.stoppuhr.pruefintervall = self.pruefinterall
        self.stoppuhr2 = Timer.Stoppuhr(0.1)

    def starten(self):
        # Erstellen der Objekten
        for warteschlangeIndex in range(8):
            warteschlange = Warteschlange.Warteschlange()
            warteschlange.warteschlangename = self.warteschlangennamen[warteschlangeIndex]
            self.warteschlangen.append(warteschlange)

        for ampelIndex in range(8):
            ampel = Ampel.Ampel()
            ampel.ampelname = self.ampelnamen[ampelIndex]
            self.ampeln.append(ampel)
        
        for index in range(len(self.ampeln)):
            self.ampeln[index].gruenphasenlaenge.clear()
            self.ampeln[index].rotphasenlaenge.clear()
        
        #Anstellwahrscheinlichkeiten
        if(len(self.anstellwahrscheinlichkeit) > 1):
            for warteschlangeIndex in range(len(self.warteschlangen)):
                self.warteschlangen[warteschlangeIndex].anstellwahrscheinlichkeit = self.anstellwahrscheinlichkeit[int(warteschlangeIndex / 4)]
        else:
            for warteschlangeIndex in range(len(self.warteschlangen)):
                self.warteschlangen[warteschlangeIndex].anstellwahrscheinlichkeit = self.anstellwahrscheinlichkeit[0]

        #Eingabe überprüfen
        if(len(self.gruenphasenlaenge) % 4 != 0 and len(self.gruenphasenlaenge) != 1):
            self.indexletztezahl = len(self.gruenphasenlaenge) % 4 
            self.gruenphasendurchlauefe = self.faktorfinden(4, len(self.gruenphasenlaenge), False)
            print(self.gruenphasendurchlauefe)
            for index in range(4 - self.indexletztezahl):
                self.gruenphasenlaenge.append(0)
            for index in range((self.gruenphasendurchlauefe * 4 ) + self.indexletztezahl, (self.gruenphasendurchlauefe * 4) + 4, 1):
                if(self.gruenphasendurchlauefe > 0):
                    self.gruenphasenlaenge[index] = self.gruenphasenlaenge[index - 4]
                else:
                    try:
                        self.gruenphasenlaenge[index] = self.gruenphasenlaenge[index + 2]
                    except:
                        self.gruenphasenlaenge[index] = self.gruenphasenlaenge[index - 2]
        elif(len(self.gruenphasenlaenge) == 1):
            for i in range(4 - 1):
                self.gruenphasenlaenge.append(self.gruenphasenlaenge[0])


        #Grünphasenkalkulation für den ersten Durchlauf
        for ampelindex in range(len(self.gruenphasenlaenge[:4])):
            self.ampeln[ampelindex * 2].gruenphasenlaenge.append(self.gruenphasenlaenge[ampelindex])
            self.ampeln[(ampelindex * 2) + 1].gruenphasenlaenge.append(self.gruenphasenlaenge[ampelindex])

        #Grünphasenkalkulation allgemein
        for durchlauf in range(int(len(self.gruenphasenlaenge) / 4)):
            for index in range(4):
                self.ampeln[index * 2].gruenphasenlaenge.append(self.gruenphasenlaenge[(durchlauf * 4 + index)])
                self.ampeln[(index * 2) + 1].gruenphasenlaenge.append(self.gruenphasenlaenge[(durchlauf * 4 + index)])

        #Rotphasenkalkulation für den ersten Durchlauf
        self.ampeln[0].rotphasenlaenge.append(0)
        self.ampeln[1].rotphasenlaenge.append(self.ampeln[0].rotphasenlaenge[0])
        self.ampeln[2].rotphasenlaenge.append(self.ampeln[0].gruenphasenlaenge[0] * self.verzoegerung)
        self.ampeln[3].rotphasenlaenge.append(self.ampeln[2].rotphasenlaenge[0]) 

        self.ampeln[4].rotphasenlaenge.append(self.ampeln[0].gruenphasenlaenge[0] * self.verzoegerung + self.ampeln[2].gruenphasenlaenge[0])
        self.ampeln[5].rotphasenlaenge.append(self.ampeln[4].rotphasenlaenge[0])
        self.ampeln[6].rotphasenlaenge.append(self.ampeln[0].gruenphasenlaenge[0] * self.verzoegerung + self.ampeln[2].gruenphasenlaenge[0] + self.ampeln[4].gruenphasenlaenge[0])
        self.ampeln[7].rotphasenlaenge.append(self.ampeln[6].rotphasenlaenge[0])

        #Rotphasenkalkulation allgemein
        for durchlauf in range(int(len(self.gruenphasenlaenge) / 4)):
            self.ampeln[0].rotphasenlaenge.append(((self.ampeln[2].gruenphasenlaenge[durchlauf]) - (self.ampeln[0].gruenphasenlaenge[durchlauf] - (self.ampeln[0].gruenphasenlaenge[durchlauf] * self.verzoegerung))) + ((self.ampeln[6].gruenphasenlaenge[durchlauf]) - (self.ampeln[4].gruenphasenlaenge[durchlauf] - (self.ampeln[4].gruenphasenlaenge[durchlauf] * self.verzoegerung)) + self.ampeln[4].gruenphasenlaenge[durchlauf]))                       
            self.ampeln[1].rotphasenlaenge.append(self.ampeln[0].rotphasenlaenge[durchlauf + 1])

            self.ampeln[2].rotphasenlaenge.append(self.verzoegerung * self.ampeln[0].gruenphasenlaenge[durchlauf] + (self.verzoegerung * self.ampeln[4].gruenphasenlaenge[durchlauf] + self.ampeln[6].gruenphasenlaenge[durchlauf])) 
            self.ampeln[3].rotphasenlaenge.append(self.ampeln[2].rotphasenlaenge[durchlauf + 1])

            self.ampeln[4].rotphasenlaenge.append(((self.ampeln[6].gruenphasenlaenge[durchlauf]) - (self.ampeln[4].gruenphasenlaenge[durchlauf] - (self.ampeln[4].gruenphasenlaenge[durchlauf] * self.verzoegerung))) + ((self.ampeln[2].gruenphasenlaenge[durchlauf]) - (self.ampeln[0].gruenphasenlaenge[durchlauf] - (self.ampeln[0].gruenphasenlaenge[durchlauf] * self.verzoegerung)) + self.ampeln[0].gruenphasenlaenge[durchlauf]))
            self.ampeln[5].rotphasenlaenge.append(self.ampeln[4].rotphasenlaenge[durchlauf + 1])

            self.ampeln[6].rotphasenlaenge.append(self.verzoegerung * self.ampeln[4].gruenphasenlaenge[durchlauf] + (self.verzoegerung * self.ampeln[0].gruenphasenlaenge[durchlauf] + self.ampeln[2].gruenphasenlaenge[durchlauf])) 
            self.ampeln[7].rotphasenlaenge.append(self.ampeln[6].rotphasenlaenge[durchlauf + 1])
               
        #Ausgabe der Kalkulationen
        rotphasenlaengeausgabe = ""
        gruenphasenlaengeausgabe = ""

        for ampel in self.ampeln:
            gruenphasenlaengeausgabe = ampel.ampelname
            rotphasenlaengeausgabe = ampel.ampelname

            for index in range(len(ampel.gruenphasenlaenge)):
                gruenphasenlaengeausgabe = "%6s %6s" %(f"{gruenphasenlaengeausgabe}", f"{round(ampel.gruenphasenlaenge[index], 2)}")
                rotphasenlaengeausgabe = "%6s %6s" %(f"{rotphasenlaengeausgabe}", f"{round(ampel.rotphasenlaenge[index], 2)}")
                
            print(f"\n{gruenphasenlaengeausgabe}")
            print(f"{rotphasenlaengeausgabe}")

        self.ampelNullGruen = False
        self.stoppuhr.start()
        for ampelIndex in range(len(self.ampeln)):
            self.ampeln[ampelIndex].start()
        self.stoppuhr2.start()

        #Simulationsprozess
        while(self.fertig == False):

            if(self.stoppuhr2.zeit() >= self.ausgabegeschwindigkeit):
                self.ausgabe()
                self.stoppuhr2.zuruecksetzen()

            if(self.ampeln[0].zustand == "Rot" and self.ampelNullGruen):
                self.durchlaeufe += 1
                self.ampelNullGruen = False

            for index in range(len(self.ampeln)):
                if(self.ampeln[index].zustand == "Grün"):
                    self.warteschlangen[index].abarbeitenstarten()
                    if(index == 0):
                        self.ampelNullGruen = True

            if(self.durchlaeufe == self.maxdurchlaufe):
                self.fertig = True
                self.stoppuhr.finish()
                self.stoppuhr2.finish()
                print("-" * 10)
                print(f"Vergangende Zeit: {self.stoppuhr.zeit()}\n")
                print("Abgearbeiteten Autos: \n")
                for warteschlange in self.warteschlangen:
                    print(f"{warteschlange.warteschlangename} {warteschlange.abgearbeitetautos}")

                for ampelIndex in range(len(self.ampeln)):
                    self.ampeln[ampelIndex].finish()

    #Hauptmemü
    def interface(self):
        print("")
        for i in range(len(self.optionen)):
            print("%0s %3s" %(f"({i})",f"{self.optionen[i][0]}"))

        try:
            self.eingabe = int(input("\nWähle Option:"))
            self.optionen[self.eingabe][1]()
        except:
            print(f"Bitte nur Zahlen zwischen 0 und {len(self.optionen)}")
            self.interface()

    def programmBeenden(self):
        print("\nProgramm wird beendet...\n")

    #Einstellungen für die Simulation
    def einstellungen(self):
        print("")

        self.standarteinstellungen = False
        self.einstellungenuebernehmen()

        for optionindex in range(len(self.einstellungenOptionen)):
            print(f"({optionindex}) {self.einstellungenOptionen[optionindex][0]}{self.einstellungenOptionen[optionindex][1]}")

        print("\nHinweis bei Grünphasenlänge: \n[Mittlere Ampel(Straße A), Linke Ampel(Straße A), Mittlere Ampel(Straße B), Linke Ampel(Straße B)]");
        print("\nHinweis bei Anstellwahrscheinlichkeit: \n[Straße A, Straße B]");

        try:
            self.eingabe = int(input("\nWähle Option: "))
            self.einstellungenOptionen[self.eingabe][1] = self.einstellungenOptionen[self.eingabe][2]()
        except:
            print(f"Bitte nur Zahlen zwischen 0 und {len(self.einstellungenOptionen)}")

        if(self.fertig == False):
            self.einstellungen()

    def einstellungenuebernehmen(self):
        with open("Save.txt", "rb") as f:
            self.datenVorhanden = pickle.load(f)

        if(self.datenVorhanden):
            self.datenLaden()

        if(len(self.einstellungenOptionen) > 0):
            self.gruenphasenlaenge = self.einstellungenOptionen[0][1]
            self.anstellwahrscheinlichkeit = self.einstellungenOptionen[1][1]
            self.pruefinterall = self.einstellungenOptionen[2][1]
            self.sekundenProAuto = self.einstellungenOptionen[3][1]
            self.verzoegerung =  self.einstellungenOptionen[4][1]
            self.ausgabegeschwindigkeit = self.einstellungenOptionen[5][1]
            self.maxdurchlaufe = self.einstellungenOptionen[6][1]
            self.stoppuhr2 = Timer.Stoppuhr(self.ausgabegeschwindigkeit)
        
        self.einstellungenOptionen =  [["Grünphasenlängen: ", self.gruenphasenlaenge , lambda: self.integerlisteaendern()], 
                                       ["Anstellwahrscheinlichkeit der Autos: ", self.anstellwahrscheinlichkeit, lambda: self.floatlisteaendern()],
                                       ["Anstellintervall der Autos: ", self.pruefinterall, lambda: self.integeraendern()],
                                       ["Durchschnittliche Abarbeitungsdauer pro Auto: ", self.sekundenProAuto, lambda: self.integeraendern()],
                                       ["Verzögerung der seitlichen Ampeln: ", self.verzoegerung, lambda: self.floataendern()],
                                       ["Ausgaben pro Sekunde: ", self.ausgabegeschwindigkeit, lambda: self.floataendern()],
                                       ["Durchläufe: ", self.maxdurchlaufe, lambda: self.integeraendern()],
                                       ["Zurück zum Hauptmenü: ", "", lambda: self.hauptmenu()]]
        self.datenVorhanden = True
        self.datenSpeichern()

    #Eine Eingabeschleife, die Eingabe des Benutzers in einer Liste speichert und erst abgebrochen wird, wenn der Benutzer den Buchstaben `e` eingibt
    def integerlisteaendern(self):
        index = 0
        eingabe = ""
        liste = []
        
        while(self.eingabeBeendet == False):
            eingabe = input(f"\nIndex {index + 1}: ")
            if(eingabe == "e" and len(self.gruenphasenlaenge) > 0):
                return liste
            if(index == 3):
                index = 0
            else: 
                index += 1
            try:
                liste.append(int(eingabe))
            except:
                print("Bitte nur ganze Zahlen oder `e` eingeben")
                self.listeaendern()

    def floatlisteaendern(self):
        index = 0
        eingabe = ""
        liste = []
        
        while(self.eingabeBeendet == False):
            eingabe = input(f"\nIndex {index + 1}: ")
            if(eingabe == "e" and len(self.gruenphasenlaenge) > 0):
                return liste
            if(index == 3):
                index = 0
            else: 
                index += 1
            try:
                liste.append(float(eingabe))
            except:
                print("Bitte nur ganze Zahlen oder `e` eingeben")
                self.listeaendern()

    #Funktionen, die die Eingabe des Benutzers zurückgeben, wenn diese den Typ entspricht
    def integeraendern(self):
        try:
            eingabe = int(input("Neuer Wert: "))
            zahl = eingabe
            print("")
            return zahl
        except:
            print("Bitte nur ganze Zahlen eingeben")
            self.integeraendern()

    def floataendern(self):
        try:
            eingabe = float(input("Neuer Wert: "))
            zahl = eingabe
            print("")
            return zahl
        except:
            print("Bitte nur Zahlen eingeben")
            self.floataendern()

    def hauptmenu(self):
        self.interface()
        return ""

    #Hier werden alle Variablen überschrieben und aktualisiert

    def autoanstellen(self):
        #Generiert eine zufällige zahl für warscheinlichkeit des anstellens
        for warteschlange in self.warteschlangen:
            self.nummer = round(random.random(), 1)
            #Wenn die generierte Zahl kleiner gleich als die Wahrscheinlichkeit ist, dann wird ein neues Auto angestellt
            if self.nummer <= warteschlange.anstellwahrscheinlichkeit:
                warteschlange.anhaengen(random.randint(self.sekundenProAuto - 1, self.sekundenProAuto + 1)) 
           
    def ausgabe(self):
        print("")
        print("-" * 10)
        for ampelIndex in range(len(self.ampeln)):
            print(f"{self.ampeln[ampelIndex].ampelname}:  {self.ampeln[ampelIndex].zustand}" )
            print(f"{self.warteschlangen[ampelIndex].warteschlangename}:  {self.warteschlangen[ampelIndex].schlange} \n")
        print("-" * 10)   

    #Findet den kleinsten Faktor von der überprüfenden Zahl und den dazugehörigen Rest
    def faktorfinden(self, faktor, ueberpruefendezahl, restausgeben):
        durchlaeufe = 0;
        zahl = ueberpruefendezahl
        while(zahl >= faktor):
                zahl = zahl - faktor
                durchlaeufe = durchlaeufe + 1 
        if(restausgeben == True):
            return zahl
        else:
            return durchlaeufe

    #Speichert die Daten in eine externe Datei 
    def datenSpeichern(self):
        with open("Save.txt", "wb") as f:
            pickle.dump(self.datenVorhanden, f)
            pickle.dump(self.gruenphasenlaenge, f)
            pickle.dump(self.anstellwahrscheinlichkeit, f)
            pickle.dump(self.pruefinterall, f)
            pickle.dump(self.sekundenProAuto, f)
            pickle.dump(self.verzoegerung, f)
            pickle.dump(self.ausgabegeschwindigkeit, f)
            pickle.dump(self.maxdurchlaufe, f)
    
    #Speichert die Daten in eine externe Datei 
    def datenLaden(self):
        with open("Save.txt", "rb") as f:
            self.daten = pickle.load(f)
            self.gruenphasenlaenge = pickle.load(f)
            self.anstellwahrscheinlichkeit = pickle.load(f)
            self.pruefinterall = pickle.load(f)
            self.sekundenProAuto = pickle.load(f)
            self.verzoegerung = pickle.load(f)
            self.ausgabegeschwindigkeit = pickle.load(f)
            self.maxdurchlaufe = pickle.load(f)

ampelkreuzung = Ampelkreuzung()
ampelkreuzung.interface()



