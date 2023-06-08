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

"""Set up window"""
xMax, yMax = 1280, 720
reso = (xMax, yMax)
surface = pg.display.set_mode(reso)
rect = surface.get_rect()

"""Get Flying V image and transform it"""
VSurface, VRect = transformimage("FlyingV.png", 0.03)

"""Define and set variables"""
xV, yV = xMax / yMax * 0.5, 0.5  # starting position
thetaV = np.pi / 2  # starting attitude
deltaThetaMaxV = 0.005  # maximum allowed change in attitude in time dt
v0, vMax = 0.5, 2  # idle velocity, max velocity with boost
vV = v0
boostTimerMax, boostTimerMin = 3, 1  # boost capacity, threshold boost level to start
acc = 4  # acceleration given by boost
boost = False  # status of boosters
boostTimer = 0  # current boost level

tSim = 0.0  # current simulated time
tStart = 0.001 * pg.time.get_ticks()  # starting time
dt = 0.001  # time step
minSleep = 0.0001  # minimum time to sleep

maxMissile = 0  # set maximum missile count
timerMaxMissile = 0  # counter for maximum missiles
timerSpawnMissile = 1  # counter for spawning missiles
missilesList = []  # list of missiles
explosionsRect = []  # boxes for explosions
explosionsFrame = []  # list for tracking explosion frames
frameTimer = 0

"""Main loop"""
pg.init()  # initialize PyGame
running = True  # condition for main loop

explosionSurfaces = [pg.transform.scale(pg.image.load("Explosion\Explosion " + str(i) + ".png"), (50, 50)) for i in
                     range(16)]

while running:
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
            missile.move(xsV, ysV, dt)  # rotate and each move missile

    """Display"""
    pg.draw.rect(surface, pg.Color("white"), rect)  # colour surface
    for missile in missilesList:
        if missile != 0:  # check if missile slot is empty
            missile.draw(surface, rect)  # draw each missile

    """Explosion handler"""
    if len(explosionsRect) > 0:  # check if there are explosions
        for explosionIndex, frame in enumerate(explosionsFrame):
            if frame <= 15:  # if the animation is not finished
                surface.blit(explosionSurfaces[frame], explosionsRect[explosionIndex])  # draw frame
                if frameTimer > 0.2:
                    explosionsFrame[explosionIndex] += 1  # step forward 1 frame
            else:
                explosionsFrame[explosionIndex] = -1

    for index, frame in enumerate(explosionsFrame):  # garbage collector
        if frame == -1:
            explosionsRect.pop(index)  # get rid of ended explosions
            explosionsFrame.pop(index)

    if frameTimer > 0.2:  # reset timer
        frameTimer = 0
    frameTimer += dt  # move timer forward

    drawobj(thetaV, xsV, ysV, surface, VSurface, VRect)
    drawboost(surface, boostTimer, boostTimerMax, xMax, yMax)
    # /\ display flying V and boost bar, more info in V functions
    pg.display.flip()  # update display

    """Timing"""
    tSim = tSim + dt
    remainder = tSim - (0.001 * pg.time.get_ticks() - tStart)
    if remainder > minSleep:
        time.sleep(remainder)

    """Counter to increase maximum missile count"""
    timerMaxMissile += dt
    if timerMaxMissile > 2:
        missilesList.append(0)  # add missile slot
        timerMaxMissile = 0

    """Missile spawning"""
    if len(missilesList) > 0:
        timerSpawnMissile += dt
    for index, missile in enumerate(missilesList):
        if missile == 0 and timerSpawnMissile > 1:
            missilesList[index] = Missile(xMax, yMax)
            timerSpawnMissile = 0

    """Collision"""
    VHitBox = gethitbox(thetaV, VRect)
    missileHitBoxes = []
    for missile in missilesList:
        if missile != 0:  # check if missile slot is empty
            missileHitBoxes.append(missile.hitbox())
        else:
            missileHitBoxes.append(pg.Rect(0, 0, 0, 0))
    #
    # if VHitBox.collidelist(missileHitBoxes) >= 0:  # check collision with V
    #     running = False

    for index, missile in enumerate(missilesList):
        if missile != 0:  # check if missile slot is empty
            for hit in missile.hitbox().collidelistall(missileHitBoxes):
                if hit != index:
                    explosionsRect.append(missilesList[hit].hitbox())
                    explosionsFrame.append(0)
                    missilesList[hit], missilesList[index] = 0, 0

    """Break loop if necessary"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False

pg.quit()
