import random
import dbk_conv_reverse as dbk_conv
import json

file = open('stbAI.json')
pi = json.load(file)
file.close()


def wuerfeln(anz):
    if anz == 1:
        ergebnis = random.randint(1, 6)
    elif anz == 2:
        ergebnis = random.randint(1, 6) + random.randint(1, 6)
    else:
        ergebnis = -1
    return ergebnis


def auswahlAktion(mAktionen, nrStrategie, klappen, wurf):
    # zustand=klappen.copy()  # wir brauchen das hier Moment nicht
    #  in mAktionen stehen alle moeglichen Aktionen – das sind mindestens 2!
    if nrStrategie == 1:  # Zufall!
        anzVarianten = len(mAktionen)
        zzahl = random.randint(0, anzVarianten-1)
        act = mAktionen[zzahl]    
    elif nrStrategie == 2:  # Florian's Schlechte Variante
        index = 0
        minElem = min(mAktionen[0])
        for i, liste in enumerate(mAktionen[1:]):
            tmpMin = min(liste)
            if minElem < tmpMin:
                minElem = tmpMin
                index = i+1
        act = mAktionen[index]
    elif nrStrategie == 3:  # Elisa's Variante
        index = 0
        maxElement = max(mAktionen[0])
        for i, liste in enumerate(mAktionen[1:]):
            tmpMax = max(liste)
            if maxElement < tmpMax:
                maxElement = tmpMax
                index = i+1
        act = mAktionen[index]  # Das ist unsere Lieblingsaktion
    elif nrStrategie == 4: # André's KI
        dezi = dbk_conv.klappenToDec(klappen)
        act = pi[dezi-1][wurf-1]
    elif nrStrategie == 5: # Hermann's KI
        anzVarianten = len(mAktionen)
        zzahl = random.randint(0, anzVarianten-1)
        act = mAktionen[zzahl]   
    return act


def auswertung(klappen, modus):
    if modus == 1:
        ergebnis = sum(klappen)
    elif modus == 2:
        ergebnis = len(klappen)
    else:
        tmp = ''
        for zahl in klappen:
            tmp += str(zahl)
        ergebnis = int(tmp)
    return ergebnis


def mVarianten(klappen, wurf):
    moeglichkeiten = [[[1]],[[2]],[[3],[1,2]],[[4],[1,3]],[[5],[1,4],[2,3]],[[6],[1,5],[2,4],[1,2,3]],[[7],[1,6],[2,5],[3,4],[1,2,4]],[[8],[1,7],[2,6],[3,5],[1,2,5],[1,3,4]],[[9],[1,8],[2,7],[3,6],[4,5],[1,2,6],[1,3,5],[2,3,4]],[[10],[1,9],[2,8],[3,7],[4,6],[1,2,7],[1,3,6],[1,4,5],[2,3,5],[1,2,3,4]],[[1,10],[2,9],[3,8],[4,7],[5,6],[1,2,8],[1,3,7],[1,4,6],[2,3,6],[2,4,5],[1,2,3,5]],[[2,10],[3,9],[4,8],[5,7],[1,5,6],[1,4,7],[1,3,8],[1,2,9],[2,4,6],[2,3,7],[3,4,5],[1,2,3,6],[1,2,4,5]]]
    moeglichkeitenWurf = moeglichkeiten[wurf-1]
    variantenListe = []
    klappenMenge = set(klappen)
    for variante in moeglichkeitenWurf:
        if set(variante).issubset(klappenMenge):
            variantenListe.append(variante)
    return variantenListe


def simulation(klappen2, n, nrS, modus):
    ergebnisse = []
    for spiele in range(n):
        klappen = list(range(1,11)) # spielen
        #klappen = klappen2.copy() # trainieren
        fertig = False
        while not fertig:
            if sum(klappen) <= 6:
                wurf = wuerfeln(1)
            else:
                wurf = wuerfeln(2)

            moeglicheVarianten = mVarianten(klappen, wurf)
            anzahlMoeglichkeiten = len(moeglicheVarianten)
            if anzahlMoeglichkeiten == 0:
                fertig = True
                ergebnis = auswertung(klappen, modus)
                ergebnisse.append(ergebnis)
            elif anzahlMoeglichkeiten == 1:
                act = moeglicheVarianten[0]
                for zahl in act:
                    klappen.remove(zahl)
            else:
                act = auswahlAktion(moeglicheVarianten, nrS, klappen, wurf)
                for zahl in act:
                    klappen.remove(zahl)
    # counter = 0
    # for i in ergebnisse:
    #     if i == 0:
    #         counter += 1
    # print(counter)
    return sum(ergebnisse)/n