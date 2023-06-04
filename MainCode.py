import pygame as pg
import time
import numpy as np

"""Set up window"""
xmax, ymax = 1280, 720
reso = (xmax, ymax)
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
x, y = xmax / ymax * 0.5, 0.5  # starting position
theta = np.pi / 2  # starting attitude
deltaThetaMax = 0.008  # maximum allowed change in attitude in time dt
v0, vmax = 0.5, 2  # idle velocity, max velocity with boost
v = v0
boostTimerMax, boostTimerMin = 3, 1  # boost capacity, treshold boost level to start
acc = 2  # acceleration given by boost
boost = False  # status of boosters
boostTimer = 0  # current boost level

tsim = 0.0  # current simulated time
tstart = 0.001 * pg.time.get_ticks()  # starting time
dt = 0.001  # time step
MINSLEEP = 0.0001  # minimum time to sleep

"""Main loop"""
pg.init()  # initialize PyGame
running = True  # condition for main loop

while running:
    tsim = tsim + dt
    if (pg.mouse.get_pressed()[0] and boostTimer >= 1) or (pg.mouse.get_pressed()[0] and boost and boostTimer >= 0):
        boost = True
        boostTimer -= dt
    else:
        boost = False
        boostTimer = min(boostTimer + dt, boostTimerMax)
    print(boostTimer)
    if boost and v < vmax:
        a = 2
    elif v > v0:
        a = -4
    else:
        a = 0

    v = v + a * dt

    vx = v * np.cos(theta)
    vy = v * np.sin(theta)
    x += vx * dt
    y += vy * dt
    xs = int(x * ymax)
    ys = ymax - int(y * ymax)
    xm, ym = pg.mouse.get_pos()
    alpha = np.arctan2(ys - ym, xm - xs)
    if alpha < 0:
        alpha += 2 * np.pi

    if 2 * np.pi - theta + alpha < abs(alpha - theta):
        deltaTheta = 2 * np.pi - theta + alpha
    elif 2 * np.pi + theta - alpha < abs(alpha - theta):
        deltaTheta = - (2 * np.pi + theta - alpha)
    else:
        deltaTheta = alpha - theta
    if abs(deltaTheta) > deltaThetaMax:
        deltaTheta = np.sign(deltaTheta) * deltaThetaMax
    theta += deltaTheta

    if theta >= 2 * np.pi:
        theta -= 2 * np.pi
    elif theta < 0:
        theta += 2 * np.pi

    thetaDeg = int(np.degrees(theta))
    VRect[thetaDeg].center = (xs, ys)
    pg.draw.rect(surface, white, rect)
    surface.blit(VSurface[thetaDeg], VRect[thetaDeg])
    pg.draw.line(surface, grey, (0.2 * xmax, 0.05 * ymax),
                 (0.8 * xmax, 0.05 * ymax))
    pg.draw.line(surface, black, (0.2 * xmax, 0.05 * ymax),
                 ((0.2 + boostTimer / boostTimerMax * 0.6) * xmax, 0.05 * ymax))
    pg.display.flip()
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)
    pg.event.pump()
pg.quit()
