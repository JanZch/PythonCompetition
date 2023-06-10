"""Basic Rules"""
# Use camelCase
# Make headers explaining what this code does
# Small comments for units, etc.
# Use the below template when defining functions
"""Function description
    -> inputs : 
    outputs ->: """

import time
from Missile import *  # missile class and methods
from VFunctions import *  # V functions, also used for missile
from menu import *  # menu stuff

"""Set up window"""
pg.init()

info = pg.display.Info()
xMax, yMax = info.current_w, info.current_h
reso = (xMax, yMax)
surface = pg.display.set_mode(reso, True)
rect = surface.get_rect()

"""Get Flying V image and transform it"""
VSurface, VRect, VRectHitbox = transformimage("FlyingV.png", 0.02, 0.5)  # image scaling, hitbox scaling
# VRectHit = pg.Rect.inflate(VRect, (-2, -2))

"""Get explosion frames"""
explosionSurfacesMissile = [pg.transform.scale(pg.image.load("Explosion\Explosion (" + str(i) + ").png"), (100, 100))
                            for i in range(1, 31)]

wholeThing = True
while wholeThing:

    """Define and set variables"""
    xV, yV = xMax / yMax * 0.5, 0.5  # starting position
    thetaV = np.pi / 2  # starting attitude
    deltaThetaMaxV = 0.06  # maximum allowed change in attitude in time dt
    v0, vMax = 0.5, 2  # idle velocity, max velocity with boost
    vV = v0
    boostTimerMax, boostTimerMin = 2, 1  # boost capacity, threshold boost level to start
    acc = 4  # acceleration given by boost
    boost = False  # status of boosters
    boostTimer = 0  # current boost level
    tSim = 0.0  # current simulated time
    tStart = 0.001 * pg.time.get_ticks()  # starting time
    dt = 0.01  # time step
    minSleep = 0.0001  # minimum time to sleep

    timerMaxMissile = 0  # counter for maximum missiles
    timerSpawnMissile = 0  # counter for spawning missiles
    timerMaxMissileLimit = 3  # how often missile list is expanded
    timerSpawnMissileLimit = 1  # how often new missile spawns (if slot available)
    timerSpawnMissileBool = False  # defines whether next missile is on queue
    posMissileInitSet = False  # defines whether initial position is set for next missile
    xMissileInit, yMissileInit = 0, 0
    missilesHardCap = 20  # max amount of possible missiles
    missilesList = [0, 0]  # list of missiles
    missilesDown = 0  # points
    explosionsRect = []  # boxes for explosions
    explosionsFrame = []  # list for tracking explosion frames
    frameTimer = 0
    borderThickness = xMax / 200  # thickness of warning frame
    borderCol = pg.Color("green")  # border colour
    textCol = pg.Color("green")
    textFont = pg.font.SysFont("courier", 25)  # text font
    background = pg.transform.scale(pg.image.load("Delftorange.jpg"),(xMax, yMax))
    openingBg = pg.transform.scale(pg.image.load("opening.jpg"),(xMax, yMax))
    endingBg = pg.transform.scale(pg.image.load("ending.jpg"),(xMax, yMax))
    gameOverBg = pg.transform.scale(pg.image.load("gameover.jpg"),(xMax, yMax))

    """Difficulty presets, [0, 1, 2, 3, 4]"""
    difficulty = 0
    difficultyMissilesHardCap = [10, 7, 8, 20, 100]
    difficultyTimerMaxMissileLimit = [5, 8, 8, 2, 0.1]
    difficultyTimerSpawnMissileLimit = [1, 0.7, 2, 0.2, 0.01]
    difficultyMissilesScale = [0, 0.1, 0.5, 0.7, 0]
    difficultyMissilesVMin = [0.25, 0.2, 0.4, 0.5, 0.25]
    difficultyMissilesVMax = [0.35, 0.5, 0.7, 0.7, 0.3]
    difficultyMissilesThetaMin = [0.02, 0.05, 0.06, 0.08, 0.02]
    difficultyMissilesThetaMax = [0.03, 0.08, 0.08, 0.1, 0.025]
    difficultyWinTime = [60, 60, 75, 90, 10]

    """Get the story text"""
    storyText = gettext("story")
    gameOverText = gettext("gameOver")
    endingText = gettext("ending")

    """Play music"""
    pg.mixer.music.load("openingmusic.mp3")
    pg.mixer.music.play(-1)

    """Running bools"""
    beginning = True
    mainGame = True
    running = False
    ending = False
    quits = False
    gameOver = False
    diffNotSet = True

    while mainGame:

        if beginning:
            surface.blit(openingBg, (0, 0))  # blit background image
            printfile(surface, storyText, textFont, textCol, xMax, yMax)  # draw the story
            contRect = pg.Rect(0.5 * xMax - 230, 0.9 * yMax, 400, 25)   # draw space to continue
            surface.blit(textFont.render("Press 1-5 to select difficulty", True, textCol), contRect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    mainGame = False
                    wholeThing = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        difficulty = 0
                        tStart = 0.001 * pg.time.get_ticks()
                        running = True
                        beginning = False
                    if event.key == pg.K_2:
                        difficulty = 1
                        tStart = 0.001 * pg.time.get_ticks()
                        running = True
                        beginning = False
                    if event.key == pg.K_3:
                        difficulty = 2
                        tStart = 0.001 * pg.time.get_ticks()
                        running = True
                        beginning = False
                    if event.key == pg.K_4:
                        difficulty = 3
                        tStart = 0.001 * pg.time.get_ticks()
                        running = True
                        beginning = False
                    if event.key == pg.K_5:
                        difficulty = 4
                        tStart = 0.001 * pg.time.get_ticks()
                        running = True
                        beginning = False
                        # starting time, put here, so you don't get hyper speed in the first few seconds
                    if event.key == pg.K_ESCAPE:
                        mainGame = False
                        wholeThing = False

        if ending:
            surface.blit(endingBg, (0, 0))
            printfile(surface, endingText, textFont, textCol, xMax, yMax)  # draw the ending
            mainGame = gameend(surface, textFont, textCol, xMax, yMax)

        if gameOver:
            surface.blit(gameOverBg, (0, 0))
            printfile(surface, gameOverText, textFont, textCol, xMax, yMax)  # draw the game over
            mainGame = gameend(surface, textFont, textCol, xMax, yMax)

        pg.display.flip()  # update display

        """Main loop"""
        while running:

            if diffNotSet:
                """Get difficulty settings"""
                missilesHardCap = difficultyMissilesHardCap[difficulty]
                timerMaxMissileLimit = difficultyTimerMaxMissileLimit[difficulty]
                timerSpawnMissileLimit = difficultyTimerSpawnMissileLimit[difficulty]
                missileScale = difficultyMissilesScale[difficulty]
                missilesVMin = difficultyMissilesVMin[difficulty]
                missilesVMax = difficultyMissilesVMax[difficulty]
                missilesDeltaThetaMin = difficultyMissilesThetaMin[difficulty]
                missilesDeltaThetaMax = difficultyMissilesThetaMax[difficulty]
                winTime = difficultyWinTime[difficulty]
                diffNotSet = False
                pg.mixer.music.load("music.mp3")
                pg.mixer.music.play(-1)

            """Inputs"""
            pressed = pg.mouse.get_pressed()[0]
            xmV, ymV = pg.mouse.get_pos()
            pg.event.pump()

            """Check for boost and increment velocity, as necessary"""
            if (pressed and boostTimer >= boostTimerMin) or \
                    (pressed and boost and boostTimer >= 0):  # only start if above boostTimerMin, but keep going until empty
                boost = True  # turn boost on
                boostTimer -= dt  # decrease boost level
            else:
                boost = False  # turn boost off
                boostTimer = min(boostTimer + dt, boostTimerMax)  # increase boost level if not already at boostTimerMax
            if boost and vV < vMax:
                a = acc  # accelerate if under vMax
            elif vV > v0:
                a = -acc  # decelerate if above v0
            else:
                a = 0  # steady speed, either v0 or vMax
            vV = vV + a * dt  # increment velocity

            """Movement"""
            xV, yV, xsV, ysV, thetaV = move(thetaV, xV, yV, xmV, ymV, deltaThetaMaxV, yMax, dt, vV)  # rotate and move V
            for missile in missilesList:
                if missile != 0:  # check if missile slot is empty
                    missile.move(xV, yV, dt, vV, thetaV)  # rotate and each move missile

            """Timing"""
            tSim = tSim + dt
            tAbs = 0.001 * pg.time.get_ticks() - tStart
            remainder = tSim - tAbs
            if remainder > minSleep:
                time.sleep(remainder)

            """Display"""
            surface.blit(background, (0, 0))  # blit background image
            for missile in missilesList:
                if missile != 0:  # check if missile slot is empty
                    missile.draw(surface, rect)  # draw each missile

            """Handle and display explosions"""
            if len(explosionsRect) > 0:  # check if there are explosions
                for explosionIndex, frame in enumerate(explosionsFrame):
                    if frame < 30:  # if the animation is not finished
                        surface.blit(explosionSurfacesMissile[frame], explosionsRect[explosionIndex])  # draw frame
                        if frameTimer > 0.05:
                            explosionsFrame[explosionIndex] += 1  # step forward 1 frame
                    else:
                        explosionsFrame[explosionIndex] = -1

            for index, frame in enumerate(explosionsFrame):  # garbage collector
                if frame == -1:
                    explosionsRect.pop(index)  # get rid of ended explosions
                    explosionsFrame.pop(index)

            if frameTimer > 0.05:  # reset timer
                frameTimer = 0
            frameTimer += dt  # move timer forward

            drawobj(thetaV, xsV, ysV, surface, VSurface, VRect, VRectHitbox)
            drawboost(surface, boostTimer, boostTimerMax, xMax, yMax)
            # /\ display flying V and boost bar, more info in V functions

            drawtext(surface, textFont, textCol, xMax, yMax, tAbs, missilesDown)

            drawborders(surface, timerSpawnMissile, timerSpawnMissileLimit, xMax, yMax, xMissileInit, yMissileInit,
                        borderThickness, borderCol)
            # /\ draw green warning borders depending on where the missile is coming from and
            # how far timerSpawnMissile has progressed since initiation

            pg.display.flip()  # update display

            """Counter to increase maximum missile count"""
            timerMaxMissile += dt
            if timerMaxMissile > timerMaxMissileLimit and len(missilesList) < missilesHardCap:
                missilesList.append(0)  # add missile slot
                timerMaxMissile = 0

            """Missile spawning"""
            # if len(missilesList) > 0:
            for index, missile in enumerate(missilesList):
                if missile == 0:  # initiate spawning if there is an empty slot in missilesList
                    timerSpawnMissileBool = True  # start spawning missile
                    if not posMissileInitSet:  # set initial position for missile being spawned
                        xMissileInit, yMissileInit = randedge()
                        posMissileInitSet = True
                    if timerSpawnMissile > timerSpawnMissileLimit:
                        missilesList[index] = Missile(xMax, yMax, xMissileInit, yMissileInit, missileScale, missilesVMin, missilesVMax, missilesDeltaThetaMin, missilesDeltaThetaMax)  # spawn missile
                        timerSpawnMissile = 0
                        timerSpawnMissileBool = False
                        posMissileInitSet = False
            if timerSpawnMissileBool:
                timerSpawnMissile += dt  # if missile being spawned, increase counter until it hits timerSpawnMissileLimit

            """Collision"""
            VHitBox = gethitbox(thetaV, VRectHitbox)
            missileHitBoxes = []
            for missile in missilesList:
                if missile != 0:  # check if missile slot is empty
                    missileHitBoxes.append(missile.hitbox())
                else:
                    missileHitBoxes.append(pg.Rect(0, 0, 0, 0))

            if VHitBox.collidelist(missileHitBoxes) >= 0:  # check collision with V
                running = False
                gameOver = True

            for index, missile in enumerate(missilesList):  # missile to missile collision
                if missile != 0:  # check if missile slot is empty
                    for hit in missile.hitbox().collidelistall(missileHitBoxes):
                        if hit != index:
                            if missilesList[index] != 0:
                                explosionsRect.append(missilesList[index].hitbox())
                                explosionsFrame.append(0)
                                missilesList[hit], missilesList[index] = 0, 0
                                missilesDown += 1

            """Win condition"""
            if tAbs > winTime:
                running = False
                ending = True

            """Break loop if necessary"""
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    gameOver = True
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                    gameOver = True

pg.quit()
