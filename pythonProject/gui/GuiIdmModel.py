"""IDM model parameters and functions"""
import random
import math

from GuiUtil import *

class IDMModel(object):

    def __init__(self, v0, T, s0, a, b):
        #Desired speed
        self.v0 = v0
        #Time headway (secs)
        self.T = T
        #Minimum gap (meters)
        self.s0 = s0
        #Acceleration (m/s)
        self.a = a
        #Deceleration (m/s)
        self.b = b
        #Multiplicator for temporary reduction
        self.alpha_v0 = 1

        self.cool = 0.99

        #possible restrictions (value 1000 => initially no restriction)
        #if effective speed limits, speedlimit<v0
        self.speedlimit = 1000
        #if vehicle restricts speed, speedmax<speedlimit, v0
        self.speedmax = 1000
        self.bmax = 16

    def calcAcc(self, s, v, vl):
        """Calculates the new acceleration
        @param s:     actual gap [m]
        @param v:     actual speed [m/s]
        @param vl:    leading speed [m/s]"""

        noiseAcc = 0.3
        accRnd = noiseAcc * (random.random() - 0.5)

        v0eff = min(self.v0, self.speedlimit, self.speedmax)
        v0eff *= self.alpha_v0

        accFree = 0

        if v < v0eff:
            accFree = self.a * (1 - math.pow(v / v0eff, 4))
        else:
            accFree = self.a * (1 - v / v0eff)

        sstar = self.s0 + v * self.T + 0.5 * v * (v - vl) / math.sqrt(self.a * self.b)
        accInt = -self.a * math.pow(sstar / max(s, self.s0), 2)

        if v0eff < 0.00001:
            return 0
        else:
            return max(-self.bmax, accFree + accInt + accRnd)

    def calcAccLg(self, s, v, vl, al):
        """Advanced calculation method
        @param s:     actual gap [m]
        @param v:     actual speed [m/s]
        @param vl:    leading speed [m/s]
        @param al:    leading acc [m/s^2]"""

        if s < 0.0001:
            return -self.bmax

        #noise to avoid some artifacts
        noiseAcc = 0.3
        accRnd = noiseAcc * (random.random() - 0.5)

        #determine valid local v0
        v0eff = min(self.v0, self.speedlimit, self.speedmax)
        v0eff *= self.alpha_v0

        #actual acceleration model
        accFree = 0

        if v < v0eff:
            accFree = self.a * (1 - math.pow(v / v0eff, 4))
        else:
            accFree = self.a * (1 - v / v0eff)

        sstar = self.s0 + v * self.T + 0.5 * v * (v - vl) / math.sqrt(self.a * self.b)
        accInt = -self.a * math.pow(sstar / max(s, self.s0), 2)
        accIDM = accFree + accInt

        accCAH = 0

        if vl * (v - vl) < -2 * s * al:
            accCAH = v * v * al / (vl * vl - 2 * s * al)
        else:
            mult = 0

            if v > vl:
                mult = 1

            accCAH = al - math.pow(v - vl, 2) / (2 * max(s, 0.01)) * mult

        accCAH = min(accCAH, self.a)

        accMix = 0

        if accIDM > accCAH:
            accMix = accIDM
        else:
            accMix = accCAH + self.b * math.tanh((accIDM - accCAH) / self.b)

        arg = (accIDM - accCAH) / self.b

        accACC = self.cool * accMix + (1 - self.cool) * accIDM

        accReturn = 0

        if v0eff < 0.00001:
            accReturn = 0
        else:
            accReturn = max(-self.bmax, accACC + accRnd)

        return accReturn
