import ShutTheBox
import json
import time
t1 = time.time()


moeglichkeiten = [[[1]],[[2]],[[3],[1,2]],[[4],[1,3]],[[5],[1,4],[2,3]],[[6],[1,5],[2,4],[1,2,3]],[[7],[1,6],[2,5],[3,4],[1,2,4]],[[8],[1,7],[2,6],[3,5],[1,2,5],[1,3,4]],[[9],[1,8],[2,7],[3,6],[4,5],[1,2,6],[1,3,5],[2,3,4]],[[10],[1,9],[2,8],[3,7],[4,6],[1,2,7],[1,3,6],[1,4,5],[2,3,5],[1,2,3,4]],[[1,10],[2,9],[3,8],[4,7],[5,6],[1,2,8],[1,3,7],[1,4,6],[2,3,6],[2,4,5],[1,2,3,5]],[[2,10],[3,9],[4,8],[5,7],[1,5,6],[1,4,7],[1,3,8],[1,2,9],[2,4,6],[2,3,7],[3,4,5],[1,2,3,6],[1,2,4,5]]]


def createPi():
    pi = []
    for i in range(0, 1023):
        pi.append([])        # Hinzufügen von 1023 leeren []
        klappen = setKlappen(i+1)
        for k in range(0, 12):
            pi[i].append([])  # Hinzufügen von 12 keeren [] für jede der 1023 []
            for j in range(0, len(moeglichkeiten[k])):
                if set(moeglichkeiten[k][j]).issubset(set(klappen)):  # Moeglichkeiten eintragen
                    pi[i][k].append(moeglichkeiten[k][j])
            if len(pi[i][k]) == 1:
                pi[i][k] = pi[i][k][0]
    return pi


def setKlappen(x):
    klappen = []
    if (x-512) >= 0:
        x -= 512
        klappen.append(10)
    if (x-256) >= 0:
        x -= 256
        klappen.append(9)
    if (x-128) >= 0:
        x -= 128
        klappen.append(8)
    if (x-64) >= 0:
        x -= 64
        klappen.append(7)
    if (x-32) >= 0:
        x -= 32
        klappen.append(6)
    if (x-16) >= 0:
        x -= 16
        klappen.append(5)
    if (x-8) >= 0:
        x -= 8
        klappen.append(4)
    if (x-4) >= 0:
        x -= 4
        klappen.append(3)
    if (x-2) >= 0:
        x -= 2
        klappen.append(2)
    if (x-1) >= 0:
        x -= 1
        klappen.append(1)
    return klappen


if __name__ == "__main__":
    pi = createPi() # Liste mit allen Optionen für alle Würfe
    pi2 = pi # Liste für este Strategie
    pi_alt = []
    for n in range(1000):
        for z in range(0, 1023):
            stellung = pi[z]
            index = 0
            for i, mAktionen in enumerate(stellung[0:]):  # optionen für speziellen wurf
                if len(mAktionen) >= 2 and not (type(mAktionen[0]) == int):
                    rest = 53
                    besteWahl = []
                    index = i
                    for option in mAktionen:  # wenn fuer wurf min 2 optionen
                        klappen2 = setKlappen(z+1)
                        for a in option:
                            klappen2.remove(a)
                        rest2 = ShutTheBox.simulation(klappen2, 2000, 3, 1)
                        if rest2 < rest:
                            rest = rest2
                            besteWahl = option
                    pi2[z][index] = besteWahl
    with open('stbAI.json', 'w') as file:
        json.dump(pi2, file)
    t2 = time.time()
    print("x Durchläufe dauerten " + str((t2-t1)/60) + " min")
