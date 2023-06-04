import pygame as pg
import time
import numpy as np

xmax, ymax = 1280, 720
reso = (xmax, ymax)
surface = pg.display.set_mode(reso)
rect = surface.get_rect()

ogVSurface = pg.image.load("FlyingV.png")
ogVSurface = pg.transform.smoothscale(ogVSurface, (73, 66))
ogVRect = ogVSurface.get_rect()
VSurface = []
VRect = []

for i in range(360):
    VSurface.append(pg.transform.rotate(ogVSurface, 180 + i))
    VRect.append(VSurface[i].get_rect())

running = True

white = (255, 255, 255)
black = (0, 0, 0)
pg.init()
x, y = xmax / ymax * 0.5, 0.5
theta = np.pi / 2
deltaThetaMax = 0.005
v0, vmax, boostTimerMax = 0.5, 2, 3
v = v0
boost = False
boostTimer = 0

tsim = 0.0
tstart = 0.001 * pg.time.get_ticks()
dt = 0.001
MINSLEEP = 0.0001

while running:
    tsim = tsim + dt
    if (pg.mouse.get_pressed()[0] and boostTimer >= 1) or (boost and boostTimer >= 0):
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
    pg.draw.line(surface, black, (0.2 * xmax, 0.1 * ymax), (boostTimer / boostTimerMax * 0.8 * xmax, 0.1 * ymax))
    pg.display.flip()
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)
    pg.event.pump()
pg.quit()
