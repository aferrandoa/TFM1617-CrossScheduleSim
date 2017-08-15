"""Traffic objects classes"""
import math
import random
import pygame
from GuiUtil import *
from GuiIdmModel import *

class GuiCar(pygame.sprite.Sprite):
    """Crossroad representation"""

    def __init__(self, ident, vector, inipos, type, is_block = False):
        pygame.sprite.Sprite.__init__(self)
        self.ident = ident
        #Original 20
        self.speed = 15

        if is_block:
            self.speed = 0
            self.image, self.rect = load_png('stop42l.png')
        else:
            self.image, self.rect = load_png('car42l.png')

        self.accl = 0
        self.status = FREE_ROAD
        #Original self.idm_model = IDMModel(self.speed, 1.4, 3, 1, 2)
        self.idm_model = IDMModel(self.speed, 1.4, 3, 0.5, 0.5)
        self.is_block = is_block

        imgrot = 0
        self.direction = type

        if type == 'E':
            imgrot = 180
        elif type == 'S':
            imgrot = 90
        elif type == 'N':
            imgrot = -90

        self.image = pygame.transform.rotate(self.image, imgrot)
        self.rect = self.image.get_rect()

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect = self.rect.move(inipos)
        self.vector = vector
        self.carsprite = pygame.sprite.RenderPlain(self)

        self.control_clock = pygame.time.Clock()
        self.entry_time = pygame.time.get_ticks()

    def update(self, lead_car, timespend):
        """Update position"""

        if not self.is_block:
            self.accl = self.calcnewacc(lead_car)
            self.speed += (self.accl)

            newpos = self.calcnewpos(self.rect, self.vector, timespend)
            self.rect = newpos

    def calcnewpos(self, rect, vector, timespend):
        """Calculate new position"""
        (angle, z) = vector
        rads = math.radians(angle)
        desp = (self.speed + (0.5 * self.accl * math.pow(timespend, 2))) * z
        #desp = mts_to_pixels(desp)
        #desp = timespend * (z * self.speed)
        (dx, dy) = (desp * math.cos(rads), desp * math.sin(rads))
        return rect.move(dx, dy)

    def calcnewacc(self, lead_car):
        """Calculates the new acceleration and velocity"""

        if lead_car != None:
            (x1, y1) = self.rect.center
            (x2, y2) = lead_car.rect.center

            dist = abs(math.hypot(x2 - x1, y2 - y1))
            #new_acc = self.idm_model.calcAcc(pixels_to_mts(dist), self.speed, lead_car.speed)
            new_acc = self.idm_model.calcAccLg(pixels_to_mts(dist), self.speed, lead_car.speed, lead_car.accl)
        else:
            #new_acc = self.idm_model.calcAcc(1000, self.speed, 120)
            new_acc = self.idm_model.calcAccLg(1000, self.speed, 120, 1)

        return new_acc

    def tickcarclock(self):
        """Gets time since last tick"""
        return self.control_clock.tick()
