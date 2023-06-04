import pygame as pg
import time
import numpy as np
from movement import *

"""Set up window"""
xMax, yMax = 1280, 720
reso = (xMax, yMax)
surface = pg.display.set_mode(reso)
rect = surface.get_rect()

"""Get Flying V image and transform it"""
ogVSurface = pg.image.load("FlyingV.png")
scale = 0.03
ogVSurface = pg.transform.smoothscale(ogVSurface,
                                      (ogVSurface.get_width() * scale, ogVSurface.get_height() * scale))  # scale down
ogVRect = ogVSurface.get_rect()

VSurface = []  # array for rotated surfaces
VRect = []  # array for rotated rectangles

for i in range(360):  # get a rotated image for all 360 degrees
    VSurface.append(pg.transform.rotate(ogVSurface, 180 + i))
    VRect.append(VSurface[i].get_rect())

"""Define and set variables"""
white, black, grey = (255, 255, 255), (0, 0, 0), (178, 190, 181)  # colours
xV, yV = xMax / yMax * 0.5, 0.5  # starting position
thetaV = np.pi / 2  # starting attitude
deltaThetaMaxV = 0.005  # maximum allowed change in attitude in time dt
v0, vmax = 0.5, 2  # idle velocity, max velocity with boost
vV = v0
boostTimerMax, boostTimerMin = 3, 1  # boost capacity, treshold boost level to start
acc = 4  # acceleration given by boost
boost = False  # status of boosters
boostTimer = 0  # current boost level

tSim = 0.0  # current simulated time
tStart = 0.001 * pg.time.get_ticks()  # starting time
dt = 0.001  # time step
minSleep = 0.0001  # minimum time to sleep

"""Main loop"""
pg.init()  # initialize PyGame
running = True  # condition for main loop

while running:
    """Inputs"""
    pressed = pg.mouse.get_pressed()[0]
    xmV, ymV = pg.mouse.get_pos()
    pg.event.pump()

    """Check for boost and increment velocity, as neccessary"""
    if (pressed and boostTimer >= boostTimerMin) or \
            (pressed and boost and boostTimer >= 0):  # only start if above boostTimerMin, but keep going until empty
        boost = True  # turn boost on
        boostTimer -= dt  # decrease boost level
    else:
        boost = False  # turn boost off
        boostTimer = min(boostTimer + dt, boostTimerMax)  # increase boost level if not already at boostTimerMax
    if boost and vV < vmax:
        a = acc  # accelerate if under vmax
    elif vV > v0:
        a = -acc  # decelerate if above v0
    else:
        a = 0  # steady speed, either v0 or vmax
    vV = vV + a * dt  # increment velocity

    xV, yV, xsV, xyV, thetaV = move(thetaV, xV, yV, xmV, ymV, deltaThetaMaxV, yMax, dt, vV)  # rotate and move V

    """Display"""
    thetaDeg = int(np.degrees(thetaV))  # get theta in degrees
    VRect[thetaDeg].center = (xsV, xyV)  # get rotated V and position it
    pg.draw.rect(surface, white, rect)  # colour surface
    surface.blit(VSurface[thetaDeg], VRect[thetaDeg])  # put V onto surface
    pg.draw.line(surface, grey, (0.2 * xMax, 0.05 * yMax),
                 (0.8 * xMax, 0.05 * yMax))  # line demarking boost capacity
    pg.draw.line(surface, black, (0.2 * xMax, 0.05 * yMax),
                 ((0.2 + boostTimer / boostTimerMax * 0.6) * xMax, 0.05 * yMax))  # line demarking boost level
    pg.display.flip()

    "Timing"
    tSim = tSim + dt
    remainder = tSim - (0.001 * pg.time.get_ticks() - tStart)
    if remainder > minSleep:
        time.sleep(remainder)

    """Break loop if neccessary"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False

pg.quit()
