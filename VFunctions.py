import random as rand

import pygame as pg
import numpy as np

"""Moved functions here to avoid looping imports which I heard can be bad
otherwise maincode -> missile -> maincode ->..."""

"""Function for image scaling (used for missile as well)
    -> inputs : pathLoc - path to the image, scaleLoc - scale to be used
    outputs ->: objSurfaceLoc - rotated surfaces, objRectLoc - rotated rectangles"""


def transformimage(pathLoc, scaleLoc):
    ogSurfaceLoc = pg.image.load(pathLoc)
    ogSurfaceLoc = pg.transform.smoothscale(ogSurfaceLoc,
                                            (ogSurfaceLoc.get_width() * scaleLoc,
                                             ogSurfaceLoc.get_height() * scaleLoc))  # scale down

    objSurfaceLoc = []  # array for rotated surfaces
    objRectLoc = []  # array for rotated rectangles

    for i in range(361):  # get a rotated image for all 360 degrees
        objSurfaceLoc.append(pg.transform.rotate(ogSurfaceLoc, 180 + i))
        objRectLoc.append(objSurfaceLoc[i].get_rect())

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


def drawborders(surfaceLoc, timerSpawnMissileLoc, timerSpawnMissileLimitLoc,
                xMaxLoc, yMaxLoc, xMissileInit, yMissileInit, borderThicknessLoc, borderColLoc):
    alpha = int(255 * timerSpawnMissileLoc / timerSpawnMissileLimitLoc)  # set opacity of red border
    if yMissileInit == 1:
        redRect1 = pg.Surface((0.6 * xMaxLoc, borderThicknessLoc))  # top
        redRect1.set_alpha(alpha)
        redRect1.fill(borderColLoc)
        surfaceLoc.blit(redRect1, (0.2 * xMaxLoc, 0))
    if yMissileInit == 0:
        redRect2 = pg.Surface((0.6 * xMaxLoc, borderThicknessLoc))  # bottom
        redRect2.set_alpha(alpha)
        redRect2.fill(borderColLoc)
        surfaceLoc.blit(redRect2, (0.2 * xMaxLoc, yMaxLoc - borderThicknessLoc))
    if xMissileInit == 0:
        redRect3 = pg.Surface((borderThicknessLoc, 0.6 * yMaxLoc))  # left
        redRect3.set_alpha(alpha)
        redRect3.fill(borderColLoc)
        surfaceLoc.blit(redRect3, (0, 0.2 * yMaxLoc))
    if xMissileInit == 16 / 9:
        redRect4 = pg.Surface((borderThicknessLoc, 0.6 * yMaxLoc))  # right
        redRect4.set_alpha(alpha)
        redRect4.fill(borderColLoc)
        surfaceLoc.blit(redRect4, (xMaxLoc - borderThicknessLoc, 0.2 * yMaxLoc))


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


def drawobj(thetaLoc, xsObjLoc, ysObjLoc, surfaceLoc, objSurfaceLoc, objRectLoc):
    thetaDeg = int(np.degrees(thetaLoc))  # get theta in degrees
    objRectLoc[thetaDeg].center = (xsObjLoc, ysObjLoc)  # get rotated V and position it
    surfaceLoc.blit(objSurfaceLoc[thetaDeg], objRectLoc[thetaDeg])  # put V onto surface
    return


def gethitbox(thetaLoc, objRectLoc):
    thetaDeg = int(np.degrees(thetaLoc))  # get theta in degrees
    return objRectLoc[thetaDeg]


def randedge():
    xMissileLoc = rand.choice((0, rand.uniform(0, 16 / 9), 16 / 9))  # choose random x coordinate
    if xMissileLoc != 0 and xMissileLoc != 16 / 9:  # if the x coordinate is not zero, set the y coordinate to zero or yMax -> top or bottom edge
        yMissileLoc = rand.choice((0, 1))
    else:
        yMissileLoc = rand.uniform(0, 1)
    return xMissileLoc, yMissileLoc
