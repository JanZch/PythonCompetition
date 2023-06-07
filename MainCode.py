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

"""Main loop"""
pg.init()  # initialize PyGame
running = True  # condition for main loop

counterMissile = 0  # placeholder for missile
missilesList = []  # list of missiles

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

    """Counter to increase maximum missile count"""
    counterMissile += dt
    if counterMissile > 5:
        maxMissile += 1
        counterMissile = 0

    """Movement"""
    xV, yV, xsV, ysV, thetaV = move(thetaV, xV, yV, xmV, ymV, deltaThetaMaxV, yMax, dt, vV)  # rotate and move V
    for missile in missilesList:
        missile.move(xsV, ysV, dt)  # rotate and each move missile

    """Display"""
    pg.draw.rect(surface, pg.Color("white"), rect)  # colour surface
    for missile in missilesList:
        missile.draw(surface, rect)  # draw each missile
    drawobj(thetaV, xsV, ysV, surface, VSurface, VRect)
    drawboost(surface, boostTimer, boostTimerMax, xMax, yMax)
    # /\ display flying V and boost bar, more info in V functions
    pg.display.flip()  # update display

    """Timing"""
    tSim = tSim + dt
    remainder = tSim - (0.001 * pg.time.get_ticks() - tStart)
    if remainder > minSleep:
        time.sleep(remainder)

    """Break loop if necessary"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False

    """Collision"""
    VHitBox = gethitbox(thetaV, VRect)
    missileHitBoxes = [missile.hitbox() for missile in missilesList]
    for index, missile in enumerate(missilesList):
        if missile != 0:
            for hit in missile.hitbox().collidelistall(missileHitBoxes):
                if hit != index:
                    missilesList[hit], missilesList[index] = 0, 0

    """Missile"""
    if len(missilesList) < maxMissile:
        missilesList.append(0)  # add missile slot
    for index, missile in enumerate(missilesList):
        if missile == 0:
            missilesList[index] = Missile(xMax, yMax)

pg.quit()
