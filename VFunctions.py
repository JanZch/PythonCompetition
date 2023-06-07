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
    ogRectLoc = ogSurfaceLoc.get_rect() # not used ?

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
    pg.draw.line(surfaceLoc, pg.Color("grey"), (0.2 * xMaxLoc, 0.05 * yMaxLoc),
                 (0.8 * xMaxLoc, 0.05 * yMaxLoc))  # line demarking boost capacity
    pg.draw.line(surfaceLoc, pg.Color("black"), (0.2 * xMaxLoc, 0.05 * yMaxLoc),
                 ((0.2 + boostTimerLoc / boostTimerMaxLoc * 0.6) * xMaxLoc, 0.05 * yMaxLoc))  # line demarking boost level
    return

"""Draws the object (V or Missile) - if drawBoostBool is set to True draws the boost 
    -> inputs : thetaLoc - rotation of the object, xsObjLoc, ysObjLoc - surface coordinates surfaceLoc, objSurfaceLoc - screen and object surface, 
                objRectLoc - object rectangle
    outputs ->: """
def drawobj(thetaLoc, xsObjLoc, ysObjLoc, surfaceLoc, objSurfaceLoc, objRectLoc):
    thetaDeg = int(np.degrees(thetaLoc))  # get theta in degrees
    objRectLoc[thetaDeg].center = (xsObjLoc, ysObjLoc)  # get rotated V and position it
    surfaceLoc.blit(objSurfaceLoc[thetaDeg], objRectLoc[thetaDeg])  # put V onto surface
    return