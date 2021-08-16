import pygame, random, math, time, os
import ShutTheBox as stb

#Pygame Init
pygame.init()
displayinfo = pygame.display.Info()

if displayinfo.current_w != -1 and displayinfo.current_h != -1:
    size = width, height = displayinfo.current_w - 200, displayinfo.current_h - 200 
    #Default (From where to scale) = (1720, 880)
else:
    size = width, height = 1000, 500

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Shut the Box')

#Logging Init
log_file = open('ShutTheBoxLog_' + time.strftime('%Y_%B_%A_%H-%M-%S') + '.txt', 'w')

#max 3 logs are saved at once for storage efficency
if not os.path.isfile('stb_logs.txt'):
    f = open('stb_logs.txt', 'w')

logs = []

with open("stb_logs.txt") as f:
    for line in f:
        logs.append(line.replace('\n', '') + '\n')

logs.append(log_file.name)

if len(logs) > 3 and logs[0] != '':
    os.remove(logs[0].replace('\n', ''))
    logs.remove(logs[0])

f = open('stb_logs.txt', 'w')
f.writelines(logs)
f.close()

#Init of variables
menustate = 1
'''1 = Main; 2 = Difficulty; 3 = In-Game'''

     #Sound
issoundenabled = True

clicksounds = [
    pygame.mixer.Sound('zapsplat_multimedia_button_click_001_68773.ogg'),
    pygame.mixer.Sound('zapsplat_multimedia_button_click_002_68774.ogg'),
    pygame.mixer.Sound('zapsplat_multimedia_button_click_003_68775.ogg'),
    pygame.mixer.Sound('zapsplat_multimedia_button_click_004_68776.ogg'),
    pygame.mixer.Sound('zapsplat_multimedia_button_click_005_68777.ogg'),
]
    #Sound End

fullscreen = False

mainmenubuttons = [None, None]
mainmenuhovers = [False, False]

diffmenubuttons = [None] * 4
diffmenuhovers = [False] * 4

checkboxlist = [None] * 2
checkboxchecks = [True, True]
checkboxhovers = [False] * 2

backbutthover = False

topcheckboxchecks = [True, False]
    
clock = pygame.time.Clock()
dt = 0
enemyturntimer = 0
enemymaxwaittime = 4

BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
GRAY = 128, 128, 128
LIGHTGRAY = 200, 200, 200
HOVER_A = 50
BG = 0, 100 , 0

currentthrow = 0
seperatethrowing = True

helpmode = True

lost = False
won = False

canenemyturn = False
canthrowdice = True

nrS = 3

klappen = [1,2,3,4,5,6,7,8,9,10]
eklappen = [1,2,3,4,5,6,7,8,9,10]
mVar = [[]].copy()
klappenToUmklappen = [[]].copy()
klappenLocked = False

woodsize = woodwidth, woodheight = int(width/10), int(height/3)
ewoodsize = eww, ewh = int(width/20), int(woodheight/2)

dicebuttsize = dbw, dbh = int(width/8), int(width/16)
dicebuttpos = dbx, dby = width/2-dbw/2, 3*dbh

bg_img = pygame.image.load('wildtextures-grey-felt-texture_blurred.jpg')
bg_img = pygame.transform.scale(bg_img, size)
checkmark = pygame.image.load('checkmark.png')
speaker_on = pygame.image.load('kisspng-sound-loudspeaker-volume-icon-5b51493458eb32.9615279515320538123642.png')
speaker_off = pygame.image.load('loudspeaker_muted.png')
# fullscreen_on = pygame.image.load('fullscreen_on.png')
# fullscreen_off = pygame.image.load('fullscreen_off.png')
ogwood = pygame.image.load('wood.jpeg')
ogborder = pygame.image.load('border.png')

backbuttpos = (0,0)
retrybuttpos = (-1000,-1000)

defbuttsize = defbw, defbh = int(width/6), int(width/12)
deffontsize = int(height/12)
defchecksize = defcw, defch = int(width/35), int(width/35) #Default is 49px

wood = pygame.image.load('wood.jpeg')
wood = pygame.transform.scale(wood, woodsize)
enemywood = pygame.image.load('wood.jpeg')
enemywood = pygame.transform.scale(enemywood, ewoodsize)
border = pygame.image.load('border.png')
border = pygame.transform.scale(border, woodsize)
enemyborder = pygame.image.load('border.png')
enemyborder = pygame.transform.scale(enemyborder, ewoodsize)

#Klappen
woodrects = []
borderrects = []
for i in range(10):
    woodrects.append(wood.get_rect())
    woodrects[i].update(width/10*i, height-woodheight, woodwidth, woodheight)
    borderrects.append(border.get_rect())
    borderrects[i].update(width/10*i, height-woodheight, 0, 0)
    
klappenavailablesurf = pygame.Surface(woodsize)
klappenavailablesurf.set_alpha(50)          
klappenavailablesurf.fill(GREEN)
klappenhoversurf = pygame.Surface(woodsize)
klappenhoversurf.set_alpha(HOVER_A)          
klappenhoversurf.fill(BLACK)

klappenhoverlist = [False] * 10
klappenavailablelist = [False] * 10

#Enemy Klappen
enemyrects = []
enemyborderrects = []
for i in range(10):
    enemyrects.append(enemywood.get_rect())
    enemyrects[i].update(width/4 + width/20*i, 0, eww, ewh)
    enemyborderrects.append(border.get_rect())
    enemyborderrects[i].update(width/4 + width/20*i, 0, 0, 0)

eklappenfont = pygame.font.SysFont('arial', 30)
eklappenschriften = []
for i in range(1,11):
    eklappenschriften.append(eklappenfont.render(str(i), True, BLACK))
eklappenschriftenmodifier = [1,1,1,1,1,1,1,1,1,1]

#Würfel Butt
dicebuttbg = pygame.transform.scale(wood, dicebuttsize)
dicebuttborderimg = pygame.transform.scale(border, dicebuttsize)
dicebutt = dicebuttbg.get_rect()
dicebutt.update(dicebuttpos, dicebuttsize)
dicebuttborder = dicebuttborderimg.get_rect()
dicebuttborder.update((dicebutt.x, dicebutt.y), dicebuttsize)

dicehoversurf = pygame.Surface(dicebuttsize)
dicehoversurf.set_alpha(HOVER_A)          
dicehoversurf.fill(BLACK)
dicehoverbool = False

#Würfel Font
dicefont = pygame.font.SysFont('arial', deffontsize)
diceschrift = dicefont.render('0', True, BLACK)

#Klappen Font
klappenfont = pygame.font.SysFont('arial', 60)
klappenschriften = []
for i in range(1,11):
    klappenschriften.append(klappenfont.render(str(i), True, BLACK))
klappenschriftenmodifier = [1,1,1,1,1,1,1,1,1,1]

#Dice
currentthrowsplit = (1,1)
def calculateCurrentThrowSplit():
    global currentthrowsplit
    currentthrowsplit = (math.floor(currentthrow/2), math.ceil(currentthrow/2))
    mVar = stb.mVarianten([1,2,3,4,5,6], currentthrow)
    buffer = (1,1)
    for pair in mVar:
        if len(pair) == 2:
            buffer = pair
            if random.random() <= 0.75:
                currentthrowsplit = pair
    if sum(klappen) <= 6 and sum(eklappen) <= 6:
        currentthrowsplit = (currentthrow, 1)
    else:
        currentthrowsplit = buffer

dicecolors = []
for i in range(6):
    dicecolors.append((random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))

#Functions
def throwDice(klappenarr, throw=-1):
    global currentthrow
    if throw == -1:
        currentthrow = stb.wuerfeln(int(sum(klappenarr) > 6) + 1)
    else:
        currentthrow = throw
    global diceschrift
    diceschrift = dicefont.render(str(currentthrow), True, BLACK)
    calculateCurrentThrowSplit()


def isKlappeOpen(arr, klappe):
    global klappenToUmklappen
    buffer = klappenToUmklappen.copy()
    klappenToUmklappen = []
    for x, lx in enumerate(arr):
        for y, ly in enumerate(lx):
            if ly == klappe:
                global klappenLocked
                klappenToUmklappen.append(lx)
                klappenLocked = True
    if len(klappenToUmklappen) >= 1:
        return True
    else:
        klappenToUmklappen = buffer.copy()
        return False


def updateEKlappen(nr):
    enemyrects[nr-1].update(enemyrects[nr-1].left,enemyrects[nr-1].top-ewh/2, 0, 0)
    enemyborderrects[nr-1].update(enemyborderrects[nr-1].left,enemyborderrects[nr-1].top-ewh/2, 0, 0)
    eklappen.remove(nr)
    eklappenschriftenmodifier[nr-1] = 0.5
            

def updateKlappen(nr):
    global klappenToUmklappen
    tempklappenToUmklappen = []
    woodrects[nr-1].update(woodrects[nr-1].left,woodrects[nr-1].top+woodheight/2, 0, 0)
    borderrects[nr-1].update(borderrects[nr-1].left,borderrects[nr-1].top+woodheight/2, 0, 0)
    klappen.remove(nr)
    for x, lx in enumerate(klappenToUmklappen):
        for y, ly in enumerate(lx):
            if ly == nr:
                tempklappenToUmklappen.insert(0, lx.copy())
                tempklappenToUmklappen[0].remove(nr)
    if tempklappenToUmklappen != []:
        klappenToUmklappen = tempklappenToUmklappen.copy()
    else:
        klappenToUmklappen = [[]].copy()
    klappenschriftenmodifier[nr-1] = 0.5
    
    
    
def resetKlappen():
    global won, lost, klappen, eklappen, backbuttpos, canenemyturn, canthrowdice, mVar, klappenToUmklappen, klappenLocked 
    
    throwDice([], 0)
    klappen = [1,2,3,4,5,6,7,8,9,10]
    eklappen = [1,2,3,4,5,6,7,8,9,10]
    for i in range(10):
        if klappenschriftenmodifier[i] == 0.5:
            woodrects[i].update((woodrects[i].left,woodrects[i].top-woodheight/2), woodsize)
            borderrects[i].update((borderrects[i].left,borderrects[i].top-woodheight/2), woodsize)
        if eklappenschriftenmodifier[i] == 0.5:
            enemyrects[i].update(enemyrects[i].left,enemyrects[i].top+ewh/2, 0, 0)
            enemyborderrects[i].update(enemyborderrects[i].left,enemyborderrects[i].top+ewh/2, 0, 0)
        klappenschriftenmodifier[i] = 1
        eklappenschriftenmodifier[i] = 1
    won = False
    lost = False
    backbuttpos = (0,0)
    
    canenemyturn = False
    canthrowdice = True
    mVar = [[]]
    klappenToUmklappen = [[]]
    klappenLocked = False
    
    
def isElemInArr(arr, e):
    for i, elem in enumerate(arr):
        if elem == e:
            return True
    return False
    

def isElemIn2DArr(arr, e):
    for x, elems in enumerate(arr):
        for y, elem in enumerate(elems):
            if elem == e:
                return True
    return False


def enemyTurn():
    moeglicheVarianten = stb.mVarianten(eklappen, currentthrow)
    anzahlMoeglichkeiten = len(moeglicheVarianten)
    print('enemyTurn(); anzahlMoeglichkeiten:' + str(anzahlMoeglichkeiten), file=log_file)
    print('enemyTurn(); mVar:' + str(moeglicheVarianten), file=log_file)
    if anzahlMoeglichkeiten == 0:
        print('enemyTurn(); Enemy Lost', file=log_file)
        global won
        won = True
    elif anzahlMoeglichkeiten == 1:
        act = moeglicheVarianten[0]
        for zahl in act:
            updateEKlappen(zahl)
    else:
        act = stb.auswahlAktion(moeglicheVarianten, nrS, eklappen, currentthrow)
        print('enemyTurn(); Act:' + str(act), file=log_file)
        for zahl in act:
            updateEKlappen(zahl)
    

def drawTextCentered(msg,color,pos,size=50, sysfont='arial'):
    '''Draws text centered around pos'''
    font_style = pygame.font.SysFont(sysfont, size)
    mesg = font_style.render(msg, True, color)
    mesgrect = mesg.get_rect(center=(pos[0], pos[1]))
    screen.blit(mesg, mesgrect)
    
def drawTextLeftTied(msg,color,pos,size=50, sysfont='arial'):
    '''Draws text from upper left corner'''
    font_style = pygame.font.SysFont(sysfont, size)
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, pos)
    
def drawDice(surface, nr=random.randint(1,6), dpos=(0, 0), dsize=(int(height/10),int(height/10)), ddradius=int(height/70), ddcolor=(0,0,0)):
    global dice1pos, dice2pos
    dicew, diceh = dsize
    dice1pos = dice1x, dice1y = dbx-2*dicew, dbh+1.5*diceh
    dice2pos = dice2x, dice2y = dbx+4*dicew, dbh+1.5*diceh
    
    dicedotsize = ddradius
    dicedotoffset = (dicew/3 - 2 * dicedotsize)/2
    
    dicedotpositions = []
    dicedotpositions.append([(3 * (dicedotsize + dicedotoffset), 3 * (dicedotsize + dicedotoffset))]) #1
    dicedotpositions.append([(1 * (dicedotsize + dicedotoffset), 1 * (dicedotsize + dicedotoffset)), (5 * (dicedotsize + dicedotoffset), 5 * (dicedotsize + dicedotoffset))]) #2
    dicedotpositions.append([]) #3
    for i in range(3):
        dicedotpositions[2].append(((1 + 2 * i) * (dicedotsize + dicedotoffset), (5 - 2 * i) * (dicedotsize + dicedotoffset)))
    dicedotpositions.append(dicedotpositions[1].copy()) #4
    dicedotpositions[3].append(dicedotpositions[2][0])
    dicedotpositions[3].append(dicedotpositions[2][2])
    dicedotpositions.append(dicedotpositions[3].copy()) #5
    dicedotpositions[4].append(dicedotpositions[0][0])
    dicedotpositions.append(dicedotpositions[3].copy()) #6
    dicedotpositions[5].append((1 * (dicedotsize + dicedotoffset), 3 * (dicedotsize + dicedotoffset)))
    dicedotpositions[5].append((5 * (dicedotsize + dicedotoffset), 3 * (dicedotsize + dicedotoffset)))
    
    pygame.draw.rect(surface, dicecolors[nr-1], pygame.Rect(dpos,dsize))
    for i, pos in enumerate(dicedotpositions[nr-1]):
        pygame.draw.circle(surface, ddcolor, (dpos[0] + pos[0], dpos[1] + pos[1]), ddradius)
        
        
def drawCheckbox(surface, checkedimg, uncheckedimg=None, toggled=True, pos=(100,100), size=(50,50), bgcolor=(255,255,255), bordercolor=(0,0,0), borderwidth=5, borderradius=0):
    '''Returns Background rect of Checkbox'''
    img = pygame.transform.scale(checkedimg, size)
    
    rect = pygame.draw.rect(surface, bgcolor, (pos, size))
    pygame.draw.rect(surface, bordercolor, (pos, size), borderwidth, borderradius)
    
    if toggled:
        screen.blit(img, (pos, size))
    elif uncheckedimg != None:
        unimg = pygame.transform.scale(uncheckedimg, size)
        screen.blit(unimg, (pos, size))
    return rect
        
def drawButtonFromImg(surface, imgsrc, pos=(0,0), size=(200,100), text='Hello World!', fontsize=deffontsize, fontsys='arial', fontcolor=(0,0,0)):
    '''Returns drawn rect'''
    img = pygame.transform.scale(imgsrc, size)
    
    rect = img.get_rect()
    rect.update(pos, size)
    
    surface.blit(img, rect)
    
    drawTextCentered(text, fontcolor, rect.center, fontsize, fontsys)
    
    return rect


def drawRectFromImg(surface, imgsrc, pos=(0,0), size=(200,100)):
    '''Returns drawn rect'''
    img = pygame.transform.scale(imgsrc, size)
    
    rect = img.get_rect()
    rect.update(pos, size)

    surface.blit(img, rect)
    
    return rect


def drawHoverEffect(surface, rect, color=(0,0,0), alpha=50):
    surf = pygame.Surface(rect.size)
    surf.set_alpha(alpha)          
    surf.fill(color)
    
    surface.blit(surf, rect)
    
def playClickSoundIfEnabled():
    if issoundenabled:
        clicksounds[random.randint(0, len(clicksounds)-1)].play()
    
#2nd Variable Init    
retrybutt = drawButtonFromImg(screen, ogwood, retrybuttpos, (0,0), 'Neustarten', 18)
retrybutthover = False

mainmenudice = []
for i in range(random.randint(2, 12)):
    mainmenudice.append([random.randint(0, 6), (random.random() * width, random.random() * height)])
diffmenudice = []
for i in range(random.randint(2, 12)):
    diffmenudice.append([random.randint(0, 6), (random.random() * width, random.random() * height)])

enemythrowtimer = 1

    #Set (Enemy)-Klappen for testing
# for nr in [3,4,5,6,7,8,9,10]:
#     updateEKlappen(nr)
    
# for nr in [5,6,7,8,9,10]:
#     updateKlappen(nr)

#Main Loop
running = True
while running:
    print('menustate: ' + str(menustate), file=log_file)
    print('klappen on begin Turn' + str(klappen) + 'E: ' + str(eklappen), file=log_file)
    screen.blit(bg_img, (0,0))
    
    topcheckboxlist = [
        drawCheckbox(screen, speaker_on, speaker_off, issoundenabled, (width-int(defcw*0.9), int(defcw*0.1)), (int(defcw*0.9), int(defch*0.9)), BG, BLACK, 3, 20)#,
        #drawCheckbox(screen, fullscreen_on, fullscreen_off, fullscreen, (width-70, 5), (30,30), BG, BLACK, 1, 0)
    ]
    
    #---Game State 1-----------------------------------------------------------------------------------------------
    if menustate == 1:
        for i in range(len(mainmenudice)):
            drawDice(screen, mainmenudice[i][0], mainmenudice[i][1])
        
        drawTextLeftTied('Sound effects obtained from https://www.zapsplat.com', BLACK, (0,0), int(deffontsize*0.35))
        drawTextLeftTied("Game by Florian Kleint", BLACK, (0,int(deffontsize*0.35)), int(deffontsize*0.35))
        
        mainmenubuttons[0] = drawButtonFromImg(screen, ogwood, (width/2-defbw/2, height/2-defbh), defbuttsize, 'Spielen')
        mainmenubuttons[1] = drawButtonFromImg(screen, ogwood, (width/2-defbw/2, height/2+defbh), defbuttsize, 'Verlassen', int(deffontsize*0.8))
        
        drawTextCentered('SHUT THE BOX', BLACK, (width/2, deffontsize*2), int(deffontsize*2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Quit
                running = False
            elif event.type == pygame.MOUSEMOTION: #Mouse Movement Event
                for i, button in enumerate(mainmenubuttons):
                    if mainmenubuttons[i].collidepoint(event.pos): #Over Spielen
                        mainmenuhovers[i] = True
                    else:
                        mainmenuhovers[i] = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #Mouse Down Event
                if mainmenubuttons[0].collidepoint(event.pos): #Spielen Click
                    menustate = 2
                    playClickSoundIfEnabled()
                elif mainmenubuttons[1].collidepoint(event.pos): #Quit Click
                    running = False
                for i, box in enumerate(topcheckboxlist):
                    if box.collidepoint(event.pos):
                        topcheckboxchecks[i] = not topcheckboxchecks[i]
                        issoundenabled = topcheckboxchecks[0]
                        #fullscreen = topcheckboxchecks[1]
        
        for i in range(len(mainmenuhovers)):
            pygame.draw.rect(screen, BLACK, mainmenubuttons[i], 4)
            if mainmenuhovers[i]:
                drawHoverEffect(screen, mainmenubuttons[i])
                
    #---Game State 2-----------------------------------------------------------------------------------------------
                
    elif menustate == 2:
        for i in range(len(diffmenudice)):
            drawDice(screen, diffmenudice[i][0], diffmenudice[i][1])
            
        backbutt = drawButtonFromImg(screen, ogwood, backbuttpos, (int(defbw/2), int(defbh/2)), 'Hauptmenü', int(deffontsize*0.35))
        pygame.draw.rect(screen, BLACK, backbutt, 2)
        
        diffmenubuttons[0] = drawButtonFromImg(screen, ogwood, (width/2-defbw, height/2-defbh*1.5), (defbw*2, int(defbh/2)), 'Rainer Zufall', int(deffontsize*0.8))
        diffmenubuttons[1] = drawButtonFromImg(screen, ogwood, (width/2-defbw, height/2-defbh*0.75), (defbw*2, int(defbh/2)), 'leicht schlechter als Elisa-rian', int(deffontsize*0.5))
        diffmenubuttons[2] = drawButtonFromImg(screen, ogwood, (width/2-defbw, height/2), (defbw*2, int(defbh/2)), 'Elisalgorithmus', int(deffontsize*0.75))
        diffmenubuttons[3] = drawButtonFromImg(screen, ogwood, (width/2-defbw, height/2+defbh*0.75), (defbw*2, int(defbh/2)), 'AIndré', int(deffontsize))
        # diffmenubuttons[4] = drawButtonFromImg(screen, ogwood, (width/2-defbw, height/2+defbh*1.5), (defbw*2, int(defbh/2)), 'Hermann: KI-ner macht mich mehr an.', int(deffontsize*0.4))
        
        checkboxlist[0] = drawCheckbox(screen, checkmark, None, checkboxchecks[0], (width/2+defcw*6.5, height/2-defch), defchecksize, (0, BG[1]+50, 0))
        drawTextLeftTied('Hilfe-Modus', BLACK, (checkboxlist[0].right+defch/5, checkboxlist[0].top), int(deffontsize*0.8))
        checkboxlist[1] = drawCheckbox(screen, checkmark, None, checkboxchecks[1], (width/2+defcw*6.5, height/2+defch), defchecksize, (0, BG[1]+50, 0))
        drawTextLeftTied('Seperates Würfeln', BLACK, (checkboxlist[1].right+defch/5, checkboxlist[1].top), int(deffontsize*0.8))
        
        drawTextCentered('SCHWIERIGKEIT', BLACK, (width/2, deffontsize*2), int(deffontsize*2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Quit
                running = False
            elif event.type == pygame.MOUSEMOTION: #Mouse Movement Event
                backbutthover = backbutt.collidepoint(event.pos)
                for i, button in enumerate(diffmenubuttons):
                    diffmenuhovers[i] = button.collidepoint(event.pos)
                for i, box in enumerate(checkboxlist):
                    checkboxhovers[i] = box.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN: #Mouse Down Event
                if backbutt.collidepoint(event.pos):
                    menustate = 1
                    backbutthover = False
                    backbuttpos = (0,0)
                    playClickSoundIfEnabled()
                    break
                for i, butt in enumerate(diffmenubuttons): #Diff Click
                    if butt.collidepoint(event.pos):
                        nrS = i+1
                        menustate = 3
                        playClickSoundIfEnabled()
                for i, box in enumerate(topcheckboxlist):
                    if box.collidepoint(event.pos):
                        topcheckboxchecks[i] = not topcheckboxchecks[i]
                        issoundenabled = topcheckboxchecks[0]
                        #fullscreen = topcheckboxchecks[1]
                for i, box in enumerate(checkboxlist): #Checkbox Click
                    if box.collidepoint(event.pos):
                        checkboxchecks[i] = not checkboxchecks[i]
                        helpmode = checkboxchecks[0]
                        seperatethrowing = checkboxchecks[1]
                            
        if backbutthover:
            drawHoverEffect(screen, backbutt)
                    
        for i in range(len(diffmenuhovers)):
            pygame.draw.rect(screen, BLACK, diffmenubuttons[i], 4)
            if diffmenuhovers[i]:
                drawHoverEffect(screen, diffmenubuttons[i])
        for i in range(len(checkboxhovers)):
            if checkboxhovers[i]:
                drawHoverEffect(screen, checkboxlist[i])
        
    #---Game State 3-----------------------------------------------------------------------------------------------
                
    elif menustate == 3:
        backbutt = drawButtonFromImg(screen, ogwood, backbuttpos, (int(defbw/2), int(defbh/2)), 'Hauptmenü', int(deffontsize*0.35))
        pygame.draw.rect(screen, BLACK, backbutt, 2)
        
        if (won or lost) and sum(klappen) == sum(eklappen):
            text = 'Unentschieden! Deine Punkte:  ' + str(sum(klappen)) + ' =  Gegnerische Punkte: ' + str(sum(eklappen))
            drawTextCentered(text, LIGHTGRAY, [width/2, height/2], 30)        
        elif (won or lost) and sum(klappen) > sum(eklappen):
            text = 'Du hast verloren! Deine Punkte:  ' + str(sum(klappen)) + ' >  Gegnerische Punkte: ' + str(sum(eklappen))
            drawTextCentered(text, RED, [width/2, height/2], 30)  
        elif (klappen == [] or won or lost) and sum(klappen) < sum(eklappen):
            won = True
            text = 'Du hast gewonnen! Deine Punkte:  ' + str(sum(klappen)) + ' <  Gegnerische Punkte: ' + str(sum(eklappen))
            drawTextCentered(text, GREEN, [width/2, height/2], 30)
        if won or lost:
            backbuttpos = (width/2 - defbw/2,height/2 + 25)
            retrybuttpos = ((width/2 + defbw/2, height/2 + 25))
            retrybutt = drawButtonFromImg(screen, ogwood, retrybuttpos, (int(defbw/2), int(defbh/2)), 'Neustarten', int(deffontsize*0.35))
            pygame.draw.rect(screen, BLACK, retrybutt, 2)
        else:
            retrybuttpos = (-1000, -1000)
            retrybutt = drawButtonFromImg(screen, ogwood, retrybuttpos, (0,0), 'Neustarten', 18)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Quit
                running = False
            elif event.type == pygame.MOUSEMOTION: #Mouse Movement Event
                backbutthover = backbutt.collidepoint(event.pos)
                retrybutthover = retrybutt.collidepoint(event.pos)
                if dicebutt.collidepoint(event.pos) and not lost and not won: #Over Dice Butt
                    dicehoverbool = True
                else:
                    dicehoverbool = False
                for i in range(10): #Over Klappen
                    if woodrects[i].collidepoint(event.pos) and isElemIn2DArr(klappenToUmklappen, i+1): #Over Klappen
                        klappenhoverlist[i] = True
                    else:
                        klappenhoverlist[i] = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #Mouse Down Event
                print('menuState == 3; Click', file=log_file)
                if backbutt.collidepoint(event.pos):
                    print('Backbutt Click', file=log_file)
                    menustate = 1
                    resetKlappen()
                    backbutthover = False
                    backbuttpos = (0,0)
                    playClickSoundIfEnabled()
                    break
                if retrybutt.collidepoint(event.pos):
                    print('Retry Click', file=log_file)
                    resetKlappen()
                    retrybutthover = False
                    playClickSoundIfEnabled()
                if dicebutt.collidepoint(event.pos): #Dice Button Click
                    print('Dice Butt Click 1', file=log_file)
                    if len(klappenToUmklappen[0]) == 0 and not lost and not won and canthrowdice:
                        print('Dice Butt Click 2', file=log_file)
                        playClickSoundIfEnabled()
                        throwDice(klappen)
                        mVar = stb.mVarianten(klappen, currentthrow)
                        if not mVar == []:
                            klappenToUmklappen = mVar.copy()
                        else:
                            klappenToUmklappen = [[]].copy()
                        klappenLocked = False
                        print('mVar:' + str(mVar), file=log_file)
                        canenemyturn = True
                        enemyturntimer = random.random() * enemymaxwaittime
                        enemythrowtimer = enemyturntimer - random.random() * enemymaxwaittime/2
                        canthrowdice = False
                        canenemythrowdice = True
                        if len(mVar) == 0:
                            lost = True
                    break
                for i, box in enumerate(topcheckboxlist):
                    if box.collidepoint(event.pos):
                        print('Top Check Click', file=log_file)
                        topcheckboxchecks[i] = not topcheckboxchecks[i]
                        issoundenabled = topcheckboxchecks[0]
                        #fullscreen = topcheckboxchecks[1]
                for i in range(10):                   #Klappen Click
                    print('Klappen Click Loop:' + str(i), file=log_file)
                    if woodrects[i].collidepoint(event.pos) and (not klappenLocked and isKlappeOpen(mVar, i+1) or (klappenLocked and isElemIn2DArr(klappenToUmklappen, i+1))): 
                        print('Klappen Click', file=log_file)
                        updateKlappen(i+1)
                        playClickSoundIfEnabled()
                        print('noch möglich.:' + str(klappenToUmklappen), file=log_file)
                        break
                print('menuState == 3; Clicks Ende', file=log_file)
                    
        if backbutthover:
            drawHoverEffect(screen, backbutt)
        if retrybutthover:
            drawHoverEffect(screen, retrybutt)
            
        # print('timer outside if:', enemyturntimer)
        if len(klappenToUmklappen[0]) == 0 and canenemyturn:
            enemyturntimer -= dt
            enemythrowtimer -= dt
            # print('timer in if:', enemyturntimer)
            if enemythrowtimer <= 0 and seperatethrowing and canenemythrowdice:
                canenemythrowdice = False
                throwDice(eklappen)
            if enemyturntimer <= 0:
                canenemyturn = False
                canthrowdice = True
                enemyTurn()
            
        for i in range(10):
            screen.blit(wood, woodrects[i]) #Klappen
            screen.blit(border, borderrects[i])
            drawTextCentered(str(i+1), BLACK, (woodwidth * i + woodwidth/2, height-woodheight/2*klappenschriftenmodifier[i]), deffontsize)
            
            screen.blit(enemywood, enemyrects[i]) #Enemy Klappen
            screen.blit(enemyborder, enemyborderrects[i])
            drawTextCentered(str(i+1), BLACK, (eww * i + width/4 + eww/2, ewh/2 * eklappenschriftenmodifier[i]), int(deffontsize*0.5) )
            #screen.blit(eklappenschriften[i], (width/4 + (width/20)*i+15,30 * eklappenschriftenmodifier[i]))
            
                
            if isElemIn2DArr(klappenToUmklappen, i+1) and helpmode: #Klappen Green Overlay
                klappenavailablelist[i] = True
            else:
                klappenavailablelist[i] = False
                
            if klappenhoverlist[i]: #Klappen Hover Overlay
                screen.blit(klappenhoversurf, borderrects[i])
            if klappenavailablelist[i]:
                screen.blit(klappenavailablesurf, borderrects[i])
        
        drawDice(screen, currentthrowsplit[0], dice1pos) #Würfel 1
        if (sum(klappen) > 6 and enemythrowtimer > 0) or (sum(eklappen) > 6 and enemythrowtimer <= 0): #Würfel 2
            drawDice(screen, currentthrowsplit[1], dice2pos)
        
        screen.blit(dicebuttbg, dicebutt) #Würfel Knopf
        screen.blit(dicebuttborderimg, dicebuttborder)
        drawTextCentered('Würfeln', BLACK, dicebutt.center, int(deffontsize*0.8))
        screen.blit(diceschrift, (dbx+dbw/2-deffontsize/4, dby-dbh))
        if dicehoverbool and len(klappenToUmklappen[0]) == 0 and canthrowdice: #Dice Hover Overlay
            screen.blit(dicehoversurf, dicebutt)
        
        #if (len(klappenToUmklappen[0]) != 0 and not canthrowdice) or lost: #Würfel Button not available overlay
        if not canthrowdice or lost:
            dicenotrollablesurf = pygame.Surface(dicebutt.size)
            dicenotrollablesurf.set_alpha(150)
            dicenotrollablesurf.fill(BLACK)
            screen.blit(dicenotrollablesurf, dicebutt)
            
    #---Game State 3-----------------------------------------------------------------------------------------------
    
    pygame.display.update()
        
    dt = clock.tick(60) / 1000
    
    print('-', file=log_file)
log_file.close()
pygame.quit()