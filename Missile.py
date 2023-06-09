"""Basic Rules"""
import numpy as np

# Use camelCase
# Make headers explaining what this code does
# Small comments for units, etc.

"""Code for the missile"""

import random as rand  # for choosing starting point
from movement import *  # for moving the missile
from VFunctions import *  # for display and image transform


class Missile:
    count = 0

    def __init__(self, xMaxInput, yMaxInput, xMissileInit, yMissileInit):  # initialize object
        """Define and set variables"""
        self.xMax, self.yMax = xMaxInput, yMaxInput  # get screen size
        self.MissileSurface, self.MissileRect = transformimage("Sidewinder.png", 0.05)  # transform image
        self.xMissile, self.yMissile = xMissileInit, yMissileInit  # get a point on the edge of the screen -> starting point
        self.thetaMissile = np.pi / 2  # starting attitude
        self.deltaThetaMaxMissile = rand.uniform(0.01, 0.1)  # maximum allowed change in attitude in time dt
        self.v0Missile = rand.uniform(0.1, 0.7)  # idle velocity
        self.vMissile = self.v0Missile  # set velocity to idle
        self.xsMissile = int(self.xMissile * self.yMax)  # surface coordinate x - not necessary but
        self.ysMissile = self.yMax - int(self.yMissile * self.yMax)  # surface coordinate y
        self.sScale = 0.3
        Missile.count += 1  # counter of how many missiles were spawned

    """Get random point on edge
        -> inputs : xMaxLoc - maximum x coordinate, yMaxLoc - maximum y coordinate
        outputs ->: xMissileLoc - missile x coordinate, yMissileLoc - missile y coordinate"""

    """Move missile to flying V
        -> inputs : xsV, ysV - screen coordinates of the V, dt - timestep
        outputs ->: none, changes the variables of the missile"""

    def move(self, xV, yV, xsV, ysV, dt, vV, thetaV):
        a = np.tan(thetaV)
        b = -1
        c = -xV + yV
        dist = abs(a * self.xMissile + b * self.yMissile + c) / np.sqrt(a ** 2 + b ** 2)
        sTarget = self.sScale * vV / self.vMissile * dist
        xTarget = xV + sTarget * np.cos(thetaV)
        yTarget = yV + sTarget * np.sin(thetaV)
        xsTarget = int(xTarget * self.yMax)
        ysTarget = self.yMax - int(yTarget * self.yMax)
        self.xMissile, self.yMissile, self.xsMissile, self.ysMissile, self.thetaMissile = \
            move(self.thetaMissile, self.xMissile, self.yMissile, xsTarget, ysTarget, self.deltaThetaMaxMissile,
                 self.yMax, dt,
                 self.vMissile)  # rotate and move missile

    """Display the missile
        -> inputs : surface - surface on which it is drawn, rect - the rect object of the surface
        outputs ->: none, draws the missile"""

    def draw(self, surface, rect):
        drawobj(self.thetaMissile, self.xsMissile, self.ysMissile, surface, self.MissileSurface, self.MissileRect)

    def hitbox(self):
        return gethitbox(self.thetaMissile, self.MissileRect)
