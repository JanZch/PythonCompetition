import pygame as pg
import time
import numpy as np

xmax, ymax = 1280, 720
reso = (xmax, ymax)
surface = pg.display.set_mode(reso)
rect = surface.get_rect()

VSurface = pg.image.load("FlyingV.png")
VSurface = pg.transform.smoothscale(VSurface, (73, 66))
VRect = VSurface.get_rect()

running = True

white = (255, 255, 255)
pg.init()
x, y = 0, 0
theta = np.pi / 2
v = 0.1

tsim = 0.0
tstart = 0.001 * pg.time.get_ticks()
dt = 0.001
MINSLEEP = 0.0001

while running:
    tsim = tsim + dt
    vx = v * np.cos(theta)
    vy = v * np.sin(theta)
    x += vx * dt
    y += vy * dt
    xs = int(x * ymax)
    ys = ymax - int(y * ymax)
    xm, ym = pg.mouse.get_pos()
    theta = np.arctan2(ys - ym, xm - xs)
    VRect.center = (xs, ys)
    pg.draw.rect(surface, white, rect)
    surface.blit(VSurface, VRect)
    pg.display.flip()
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)
    pg.event.pump()
pg.quit()
