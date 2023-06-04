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
deltaThetaMax = 0.005  # maximum allowed change in attitude in time dt
v0, vmax = 0.5, 2  # idle velocity, max velocity with boost
v = v0
boostTimerMax, boostTimerMin = 3, 1  # boost capacity, treshold boost level to start
acc = 4  # acceleration given by boost
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
    """Inputs"""
    pressed = pg.mouse.get_pressed()[0]
    xm, ym = pg.mouse.get_pos()
    pg.event.pump()

    """Check for boost and increment velocity, as neccessary"""
    if (pressed and boostTimer >= boostTimerMin) or \
            (pressed and boost and boostTimer >= 0):  # only start if above boostTimerMin, but keep going until empty
        boost = True  # turn boost on
        boostTimer -= dt  # decrease boost level
    else:
        boost = False  # turn boost off
        boostTimer = min(boostTimer + dt, boostTimerMax)  # increase boost level if not already at boostTimerMax
    if boost and v < vmax:
        a = acc  # accelerate if under vmax
    elif v > v0:
        a = -acc  # decelerate if above v0
    else:
        a = 0  # steady speed, either v0 or vmax
    v = v + a * dt  # increment velocity

    """Change position"""
    vx = v * np.cos(theta)
    vy = v * np.sin(theta)
    x += vx * dt  # relative coordinates
    y += vy * dt
    xs = int(x * ymax)  # surface coordinates
    ys = ymax - int(y * ymax)

    """Steer depending on location of mouse pointer"""
    alpha = np.arctan2(ys - ym, xm - xs)  # get angle of pointer wrt V
    if alpha < 0:  # convert -pi pi range of atan2 to 0 2pi
        alpha += 2 * np.pi
    if 2 * np.pi - theta + alpha < abs(alpha - theta):  # if angle has to go from under to above x axis
        deltaTheta = 2 * np.pi - theta + alpha
    elif 2 * np.pi + theta - alpha < abs(alpha - theta):  # if angle has to go from above to under the x axis
        deltaTheta = - (2 * np.pi + theta - alpha)
    else:
        deltaTheta = alpha - theta  # if neither are needed
    if abs(deltaTheta) > deltaThetaMax:  # limit rate of turn per time step
        deltaTheta = np.sign(deltaTheta) * deltaThetaMax
    theta += deltaTheta  # adjust angle by rate of turn

    """Correct angle if out of bound"""
    if theta >= 2 * np.pi:
        theta -= 2 * np.pi
    elif theta < 0:
        theta += 2 * np.pi

    """Display"""
    thetaDeg = int(np.degrees(theta))  # get theta in degrees
    VRect[thetaDeg].center = (xs, ys)  # get rotated V and position it
    pg.draw.rect(surface, white, rect)  # colour surface
    surface.blit(VSurface[thetaDeg], VRect[thetaDeg])  # put V onto surface
    pg.draw.line(surface, grey, (0.2 * xmax, 0.05 * ymax),
                 (0.8 * xmax, 0.05 * ymax))  # line demarking boost capacity
    pg.draw.line(surface, black, (0.2 * xmax, 0.05 * ymax),
                 ((0.2 + boostTimer / boostTimerMax * 0.6) * xmax, 0.05 * ymax))  # line demarking boost level
    pg.display.flip()

    "Timing"
    tsim = tsim + dt
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)

    """Break loop if neccessary"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False

pg.quit()
