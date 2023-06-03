import pygame as pg

xmax, ymax = 1280, 720
reso = (xmax, ymax)
screen = pg.display.set_mode(reso)
running = True

pg.init()

while running:

    # xs = int(x / 1.2 * xmax)
    # ys = ymax - int(y * ymax)

pg.quit()
