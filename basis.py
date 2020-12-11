from typing import List, Any

import pygame, sys, time, random, math
from pygame.locals import *

WIDTH       = 1024
hWIDTH      = WIDTH/2
HEIGHT      = 768
base        = 64

WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (255, 0, 0)

mainsurf    = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

fpsClock    = pygame.time.Clock()
FPS         = 30

G           = -6
JUMPSPEED   = 50
PLAYERSPEED = 10

pATTACK     = 0
pJUMP       = 1
pNOMAL      = 2
#           uuid, priority
IDLE        = [0, pNOMAL]
MOVING      = [1, pNOMAL]
JUMPUP      = [2, pJUMP]
JUMPDOWN    = [3, pJUMP]
ATTACK      = [4, pATTACK]

IDLEINTERVAL= 0.8
MOVEINTERVAL= 0.1
ATTACKINTERVAL = 0.1
NOINTERVAL  = 0
INVINCIBILITYINTERVAL = 0.08

INVINCIBILITYTIME = 0.7

k_left      = K_a
k_right     = K_d
k_down      = K_s
k_jump      = K_k
k_rush      = K_l
k_attack    = K_j
k_pause     = K_p

list_platform= []
list_enemy  = []

class Box:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def setPosition(self, centerx, y):
        self.centerx = centerx
        self.y = y
        self.boxUpdate()
    def moving(self, vx, vy):
        self.centerx += vx
        self.y += vy
        self.boxUpdate()
    def boxUpdate(self):
        # compute 'x', 'xr', 'top' using 'centerx' and 'y'
        self.x = self.centerx - self.w/2
        self.xr = self.centerx + self.w/2
        self.top = self.y + self.h
        self.coord()
    def coord(self):
        self.drawy = HEIGHT - self.y - self.h
    def isCollideWith(self, box2):
        if box2.top > self.y and box2.y < self.top and box2.xr > self.x and box2.x < self.xr:
            return True
        return False

class MovableObj():
    def __init__(self):
        # facing: 0 for left, 1 for right
        self.facing = 0
        self.attacking = 0
        self.state = IDLE
        self.onground = 1
        self.jumptimes = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

class StillObj:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.coord()
    def coord(self):
        w, h = self.img.get_size()
        self.drawy = HEIGHT - self.y - h
    def draw(self):
        mainsurf.blit(self.img, (self.x, self.drawy))

def collisionDetect(movable):
    for i in list_platform:
        if movable.box.x < i.rect_r and movable.box.xr > i.rect_l:
            if i.rect_t <= movable.box.y and i.rect_t > movable.box.y + movable.vy + G:
                movable.box.y = i.rect_t
                movable.landing()
                return
    movable.onground = 0
    movable.ay = G
    movable.vy += movable.ay
