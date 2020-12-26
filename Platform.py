import pygame
from pygame.locals import *

from basis import *

class Platform(StillObj):
    def __init__(self, index, img, x, y):
        StillObj.__init__(self, img, x, y)
        w, h = img.get_size()
        self.rect_t = y + h
        self.rect_l = x
        self.rect_r = x + w
        self.index = index
        self.reach = []
        self.route = []
