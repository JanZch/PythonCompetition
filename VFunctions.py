import random as rand

import pygame as pg
import numpy as np

"""Moved functions here to avoid looping imports which I heard can be bad
otherwise maincode -> missile -> maincode ->..."""

"""Function for image scaling (used for missile as well)
    -> inputs : pathLoc - path to the image, scaleLoc - scale to be used
    outputs ->: objSurfaceLoc - rotated surfaces, objRectLoc - rotated rectangles"""


def transformimage(pathLoc, scaleLoc, scaleHitboxLoc=0):
    ogSurfaceLoc = pg.image.load(pathLoc)
    ogSurfaceLoc = pg.transform.smoothscale(ogSurfaceLoc,
                                            (ogSurfaceLoc.get_width() * scaleLoc,
                                             ogSurfaceLoc.get_height() * scaleLoc))  # scale down

    objSurfaceLoc = []  # array for rotated surfaces
    objRectLoc = []  # array for rotated rectangles
    objHitboxLoc = []  # array for scaled rectangles for hitbox

    for i in range(361):  # get a rotated image for all 360 degrees
        objSurfaceLoc.append(pg.transform.rotate(ogSurfaceLoc, 180 + i))
        objRectLoc.append(objSurfaceLoc[i].get_rect())

    if scaleHitboxLoc != 0:
        for i in range(361):
            objHitboxLoc.append(pg.Rect.scale_by(objRectLoc[i], scaleHitboxLoc, scaleHitboxLoc))
        return objSurfaceLoc, objRectLoc, objHitboxLoc
    else:
        return objSurfaceLoc, objRectLoc


"""Draws the boost bar
    -> inputs : surfaceLoc - surface on which it is drawn, boostTimerLoc, boostTimerMaxLoc - boost timer, xMaxLoc, yMaxLoc - maximum screen coordinates
    outputs ->: none, draws the boost bar"""


def drawboost(surfaceLoc, boostTimerLoc, boostTimerMaxLoc, xMaxLoc, yMaxLoc):
    # pg.draw.line(surfaceLoc, pg.Color("grey"), (0.2 * xMaxLoc, 0.05 * yMaxLoc),
    #              (0.8 * xMaxLoc, 0.05 * yMaxLoc))  # line demarking boost capacity
    pg.draw.line(surfaceLoc, pg.Color("green"), (0.2 * xMaxLoc, 0.05 * yMaxLoc),
                 ((0.2 + boostTimerLoc / boostTimerMaxLoc * 0.6) * xMaxLoc,
                  0.05 * yMaxLoc))  # line demarking boost level
    return


"""Draws the warning borders
    -> inputs : surfaceLoc - surface on which it is drawn, timerSpawnMissileLoc, timerSpawnMissileLimitLoc - spawn timer, xMaxLoc, yMaxLoc - maximum screen coordinates, xMissileInit, yMissileInit - missile spawn coordinates, borderThicknessLoc - thickness of borders, borderColLoc - colour of borders
    outputs ->: none, draws the warning borders"""


def drawborders(surfaceLoc, timerSpawnMissileLoc, timerSpawnMissileLimitLoc,
                xMaxLoc, yMaxLoc, xMissileInit, yMissileInit, borderThicknessLoc, borderColLoc):
    alpha = int(255 * timerSpawnMissileLoc / timerSpawnMissileLimitLoc)
    # /\ get opacity of border depending on spawn timer progress
    if yMissileInit == 1:  # spawning at the top
        borderSurface = pg.Surface((0.6 * xMaxLoc, borderThicknessLoc))  # get surface and size it
        borderSurface.set_alpha(alpha)  # set opacity of surface
        borderSurface.fill(borderColLoc)  # fill surface with borderColLoc
        surfaceLoc.blit(borderSurface, (0.2 * xMaxLoc, 0))  # position surface on background
    if yMissileInit == 0:  # spawning at the bottom
        borderSurface = pg.Surface((0.6 * xMaxLoc, borderThicknessLoc))
        borderSurface.set_alpha(alpha)
        borderSurface.fill(borderColLoc)
        surfaceLoc.blit(borderSurface, (0.2 * xMaxLoc, yMaxLoc - borderThicknessLoc))
    if xMissileInit == 0:  # spawning on the left
        borderSurface = pg.Surface((borderThicknessLoc, 0.6 * yMaxLoc))
        borderSurface.set_alpha(alpha)
        borderSurface.fill(borderColLoc)
        surfaceLoc.blit(borderSurface, (0, 0.2 * yMaxLoc))
    if xMissileInit == 16 / 9:  # spawning on the right
        borderSurface = pg.Surface((borderThicknessLoc, 0.6 * yMaxLoc))
        borderSurface.set_alpha(alpha)
        borderSurface.fill(borderColLoc)
        surfaceLoc.blit(borderSurface, (xMaxLoc - borderThicknessLoc, 0.2 * yMaxLoc))


def drawtext(surfaceLoc, textFontLoc, textColLoc, xMaxLoc, yMaxLoc, tAbsLoc, missilesDownLoc):
    timeLabel = textFontLoc.render(str(round(tAbsLoc, 2)), True, textColLoc)
    timeLabelRect = timeLabel.get_rect()
    timeLabelRect.left = 0.2 * xMaxLoc
    timeLabelRect.top = 0.05 * yMaxLoc
    surfaceLoc.blit(timeLabel, timeLabelRect)

    pointsLabel = textFontLoc.render(str(missilesDownLoc), True, textColLoc)
    pointsLabelRect = pointsLabel.get_rect()
    pointsLabelRect.right = 0.8 * xMaxLoc
    pointsLabelRect.top = 0.05 * yMaxLoc
    surfaceLoc.blit(pointsLabel, pointsLabelRect)


"""Draws the object (V or Missile) - if drawBoostBool is set to True draws the boost 
    -> inputs : thetaLoc - rotation of the object, xsObjLoc, ysObjLoc - surface coordinates surfaceLoc, objSurfaceLoc - screen and object surface, 
                objRectLoc - object rectangle
    outputs ->: """


def drawobj(thetaLoc, xsObjLoc, ysObjLoc, surfaceLoc, objSurfaceLoc, objRectLoc, objHitboxLoc=0):
    thetaDeg = int(np.degrees(thetaLoc))  # get theta in degrees
    objRectLoc[thetaDeg].center = (xsObjLoc, ysObjLoc)  # get rotated object and position it
    if objHitboxLoc != 0:
        objHitboxLoc[thetaDeg].center = (xsObjLoc, ysObjLoc)
    surfaceLoc.blit(objSurfaceLoc[thetaDeg], objRectLoc[thetaDeg])  # put object onto surface
    return


def gethitbox(thetaLoc, objRectLoc):
    thetaDeg = int(np.degrees(thetaLoc))  # get theta in degrees
    return objRectLoc[thetaDeg]


"""Get random point on edge
    -> inputs : 
    outputs ->: xMissileLoc - missile x coordinate, yMissileLoc - missile y coordinate"""


def randedge():
    xMissileLoc = rand.choice((0, rand.uniform(0, 16 / 9), 16 / 9))  # choose random x coordinate
    if xMissileLoc != 0 and xMissileLoc != 16 / 9:
        # if the x coordinate is not zero, set the y coordinate to zero or yMax -> top or bottom edge
        yMissileLoc = rand.choice((0, 1))
    else:
        yMissileLoc = rand.uniform(0, 1)
    return xMissileLoc, yMissileLoc
