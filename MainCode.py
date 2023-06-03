import pygame as pg

xmax, ymax = 1280, 720
reso = (xmax, ymax)
surface = pg.display.set_mode(reso)

VSurface = pg.image.load("FlyingV.png")
VSurface = pg.transform.scale(VSurface, (50, 55))
VRect = VSurface.get_rect()

running = True

pg.init()

while running:
    VRect.center = (500, 500)
    surface.blit(VSurface, VRect)
    pg.display.flip()

# xs = int(x / 1.2 * xmax)
# ys = ymax - int(y * ymax)

pg.quit()
