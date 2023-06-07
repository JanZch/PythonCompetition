"""Basic Rules"""
# Use camelCase
# Make headers explaining what this code does
# Small comments for units, etc.

"""Code for the missile"""

import random as rand # for choosing starting point
from movement import * # for moving the missile
from VFunctions import * # for display and image transform

class Missile:
    count = 0
    def __init__(self, xMaxInput, yMaxInput): # initialize object
        """Define and set variables"""
        self.xMax, self.yMax = xMaxInput, yMaxInput # get screen size
        self.MissileSurface, self.MissileRect = transformimage("Sidewinder.png",0.03) # transform image
        self.xMissile, self.yMissile = self.randedge() # get a point on the edge of the screen -> starting point
        self.thetaMissile = np.pi / 2  # starting attitude
        self.deltaThetaMaxMissile = 0.005  # maximum allowed change in attitude in time dt
        self.v0Missile = 0.3  # idle velocity
        self.vMissile = self.v0Missile # set velocity to idle
        self.xsMissile = int(self.xMissile * self.yMax)  # surface coordinate x - not necessary but
        self.ysMissile = self.yMax - int(self.yMissile * self.yMax) # surface coordinate y
        Missile.count += 1

    """Get random point on edge
        -> inputs : xMaxLoc - maximum x coordinate, yMaxLoc - maximum y coordinate
        outputs ->: xMissileLoc - missile x coordinate, yMissileLoc - missile y coordinate"""
    def randedge(self):
        xMissileLoc = rand.choice((0,rand.uniform(0,16/9))) # choose random x coordinate
        if xMissileLoc != 0: # if the x coordinate is not zero, set the y coordinate to zero or yMax -> top or bottom edge
            yMissileLoc = rand.choice((0,1))
        else:
            yMissileLoc = rand.uniform(0,1)
        return xMissileLoc, yMissileLoc

    """Move missile to flying V
        -> inputs : xsV, ysV - screen coordinates of the V, dt - timestep
        outputs ->: none, changes the variables of the missile"""
    def move(self, xsV, ysV, dt):
        self.xMissile, self.yMissile, self.xsMissile, self.ysMissile, self.thetaMissile = \
            move(self.thetaMissile, self.xMissile, self.yMissile, xsV, ysV, self.deltaThetaMaxMissile, self.yMax, dt, self.vMissile)  # rotate and move missile

    """Display the missile
        -> inputs : surface - surface on which it is drawn, rect - the rect object of the surface
        outputs ->: none, draws the missile"""
    def draw(self, surface, rect):
        drawobj(self.thetaMissile, self.xsMissile, self.ysMissile, surface, self.MissileSurface, self.MissileRect)

    def hitbox(self):
        return gethitbox(self.thetaMissile, self.MissileRect)