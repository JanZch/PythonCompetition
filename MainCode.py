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
pg.init()
x, y = xmax / ymax * 0.5, 0.5
theta = np.pi / 2
deltaThetaMax = 0.005
v0, vmax = 0.5, 1
v = v0

tsim = 0.0
tstart = 0.001 * pg.time.get_ticks()
dt = 0.001
MINSLEEP = 0.0001

while running:
    tsim = tsim + dt
    boost = pg.mouse.get_pressed()[0]
    if boost == True and not v >= vmax:
        a = 1
    elif v > v0:
        a = -1
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
        print("lentrol fel")
    elif 2 * np.pi + theta - alpha < abs(alpha - theta):
        deltaTheta = - (2 * np.pi + theta - alpha)
        print("fentrol le")
    else:
        deltaTheta = alpha - theta
    if abs(deltaTheta) > deltaThetaMax:
        deltaTheta = np.sign(deltaTheta) * deltaThetaMax
    print(deltaTheta)

    theta += deltaTheta

    if theta >= 2 * np.pi:
        theta -= 2 * np.pi
    elif theta < 0:
        theta += 2 * np.pi

    thetaDeg = int(np.degrees(theta))
    VRect[thetaDeg].center = (xs, ys)
    pg.draw.rect(surface, white, rect)
    surface.blit(VSurface[thetaDeg], VRect[thetaDeg])
    pg.display.flip()
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)
    pg.event.pump()
pg.quit()
