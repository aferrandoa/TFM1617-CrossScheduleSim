"""Util functions"""
import os
import math
import pygame
from GuiConstants import *

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('.', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()

def kmh_to_ms(in_kmh):
    """ Converts km/h to m/s """
    return in_kmh * 0.2777778

def ms_to_kmh(in_ms):
    """ Converts m/s to km/h"""
    return in_ms * 3.600

def mts_to_pixels(in_mts):
    """ Converts meters to pixels """
    return in_mts * APP_SCALE

def pixels_to_mts(in_pixels):
    """ Converts pixels to meters """
    return in_pixels / APP_SCALE

def distance_rects(rect1, rect2):
    """Returns the distance between 2 rects"""

    (x1, y1) = rect1.center
    (x2, y2) = rect2.center

    return math.hypot(x2 - x1, y2 - y1)
    