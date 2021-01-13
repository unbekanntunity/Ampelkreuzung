#-------------------------------------------------------------------------------
# Name:        Ampelkreuzung
# Purpose:     Simulation einer Ampel
#
# Author:      T.nguyen, T. Rothe 
#
# Created:     13.01.2020
# Copyright:   (c) an.nguyen 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Timer 
import Ampel 
import Warteschlange 

anstellWahrscheinlichkeit = 0.5
maxdurchlaufe = 10
grunphasenlaenge = [ 5 , 3 , 5 , 3 ]

#A1 = grunphasenlaenge[2] * 0.8 + grunphasenlaenge[3] + 1 - grunphasenlaenge[0] *  0.8

#jede ampel braucht timer der immer gestartet wird wenn die ampel umschaltet

#warteschlangeA11  0
#warteschlangeA12  1
#warteschlangeA21  2
#warteschlangeA22  3
#warteschlangeB11  4
#warteschlangeB12  5
#warteschlangeB21  6
#warteschlangeB22  7

anzahlWarteschlangen = 8
warteschlangen = []

for warteschlange in range(anzahlWarteschlangen):
    warteschlange = Warteschlange.Warteschlange()
    warteschlangen.append(warteschlange)
