"""Basic Rules"""

# Use camelCase
# Make headers explaining what this code does
# Small comments for units, etc.

"""Code for the missile"""

from movement import *  # for moving the missile
from VFunctions import *  # for display and image transform


class Missile:
    count = 0

    def __init__(self, xMaxInput, yMaxInput, xMissileInit, yMissileInit):  # initialize object
        """Define and set variables"""
        self.xMax, self.yMax = xMaxInput, yMaxInput  # get screen size
        self.MissileSurface, self.MissileRect = transformimage("Sidewinder.png", 0.05)  # transform image
        self.xMissile, self.yMissile = xMissileInit, yMissileInit
        # /\ get a point on the edge of the screen -> starting point
        self.thetaMissile = np.pi / 2  # starting attitude
        self.deltaThetaMaxMissile = rand.uniform(0.01, 0.1)  # maximum allowed change in attitude in time dt
        self.v0Missile = rand.uniform(0.1, 0.7)  # idle velocity
        self.vMissile = self.v0Missile  # set velocity to idle
        self.xsMissile = int(self.xMissile * self.yMax)  # surface coordinate x - not necessary but
        self.ysMissile = self.yMax - int(self.yMissile * self.yMax)  # surface coordinate y
        self.sScale = 0.3  # constant scaling factor for targeting overshoot
        Missile.count += 1  # counter of how many missiles were spawned

    """Move missile to flying V
        -> inputs : xsV, ysV - screen coordinates of the V, dt - timestep,
        vV - Flying V velocity, thetaV - Flying V attitude
        outputs ->: none, changes the variables of the missile"""

    def move(self, xV, yV, dt, vV, thetaV):
        a = np.tan(thetaV)  # get equation of instantaneous line on which V is travelling
        b = -1
        c = -xV + yV
        dist = abs(a * self.xMissile + b * self.yMissile + c) / np.sqrt(a ** 2 + b ** 2)
        # /\ get how far missile is from line
        sTarget = self.sScale * vV / self.vMissile * dist
        # /\ scale overshoot distance with sScale (constant factor), vV / vMissile, and dist
        xTarget = xV + sTarget * np.cos(thetaV)  # get target x and y components of overshoot based on Flying V attitude
        yTarget = yV + sTarget * np.sin(thetaV)
        xsTarget = int(xTarget * self.yMax)  # convert to screen coordinates
        ysTarget = self.yMax - int(yTarget * self.yMax)
        self.xMissile, self.yMissile, self.xsMissile, self.ysMissile, self.thetaMissile = \
            move(self.thetaMissile, self.xMissile, self.yMissile, xsTarget, ysTarget, self.deltaThetaMaxMissile,
                 self.yMax, dt,
                 self.vMissile)  # rotate and move missile to target coordinates

    """Display the missile
        -> inputs : surface - surface on which it is drawn, rect - the rect object of the surface
        outputs ->: none, draws the missile"""

    def draw(self, surface, rect):
        drawobj(self.thetaMissile, self.xsMissile, self.ysMissile, surface, self.MissileSurface, self.MissileRect)

    def hitbox(self):
        return gethitbox(self.thetaMissile, self.MissileRect)
