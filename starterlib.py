from typing import List, Any

import pygame, sys, time, random, math
from pygame.locals import *

WIDTH       = 768
HEIGHT      = 512
hWIDTH      = WIDTH/2

WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (255, 0, 0)

#BASICFONT   = pygame.font.Font('freesansbold.ttf', 32)

mainsurf    = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

fpsClock    = pygame.time.Clock()
FPS         = 30

G           = -10
PLAYERSPEED = 10

IDLE        = 0
MOVING      = 1

list_madness= []
list_still = []
list_player = []
list_enemy  = []

class StillObj:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.coord()
    def coord(self):
        w, h = self.img.get_size()
        self.y = HEIGHT - self.y - h
    def draw(self):
        mainsurf.blit(self.img, (self.x, self.y))

class MovableObj:
    def __init__(self, x, y, vx, vy, ax, ay, facing):
        self.x = x
        self.y = y
        # state: 0 for idle, 1 for moving
        self.state = 0
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        # facing: 0 for left, 1 for right
        self.facing = facing

class Player(MovableObj):
    def __init__(self, pic):
        self.pic = pic
        self.picnum = len(pic)
        self.picindex = 0
        self.w, self.h = pic[0][0][0].get_size()
        MovableObj.__init__(self, hWIDTH - self.w/2, HEIGHT - 64 - self.h, 0, 0, 0, 0, 1)
    def update(self, direction):
        if direction > 0 and self.x + self.w < WIDTH:
            self.vx = PLAYERSPEED
            self.state = 1
            self.facing = 1
        elif direction < 0 and self.x > 0:
            self.vx = -PLAYERSPEED
            self.state = 1
            self.facing = 0
        else:
            self.vx = 0
            self.state = 0
        self.x += self.vx
        self.picindex = (self.picindex + 1) % 20
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state][int(self.picindex/5)], (self.x, self.y))
