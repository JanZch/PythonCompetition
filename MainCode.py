import pygame as pg
import time

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


tsim = 0.0
tstart = 0.001 * pg.time.get_ticks()
dt = 0.1


while running:
    trun = 0.001 * pg.time.get_ticks() - tstart
    if trun + dt >= tsim:
        x += 0.01
        y += 0.01
        xs = int(x * ymax)
        ys = ymax - int(y * ymax)
        VRect.center = (xs, ys)
        pg.draw.rect(surface, white, rect)
        surface.blit(VSurface, VRect)
        pg.display.flip()
        time.sleep(0.1)

pg.quit()
