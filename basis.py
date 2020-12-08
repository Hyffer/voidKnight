from typing import List, Any

import pygame, sys, time, random, math
from pygame.locals import *

WIDTH       = 1024
hWIDTH      = WIDTH/2
HEIGHT      = 768
base        = 64
initx       = hWIDTH
inity       = 128

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
ATTACKINTERVAL = 0.4
NOINTERVAL  = 0

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
    def __init__(self, x, y, w, h):
        self.h = h
        self.w = w
        self.x = x - w/2
        self.y = y
        self.boxUpdate()
    def boxUpdate(self):
        self.centerx = self.x + self.w/2
        self.top = self.y + self.h
        self.xr = self.x + self.w
        self.coord()
    def coord(self):
        self.drawy = HEIGHT - self.y - self.h
    def collidebox(self, box2):
        if box2.top > self.y and box2.y < self.top and box2.xr > self.x and box2.x < self.xr:
            return True

class MovableObj():
    def __init__(self, pic, x, y):
        # picture manage
        self.pic = pic
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        # collision box init
        w, h = pic[0][0][0].get_size()
        self.box = Box(x, y, w, h)
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
