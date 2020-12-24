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
GREEN       = (0, 255, 0)
FONTTITLE = './resources/fonts/Supernatural_Knight.ttf'
FONT = './resources/fonts/Trajan.otf'

mainsurf    = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
mistrect    = pygame.Surface((WIDTH, HEIGHT))
mistrect.set_alpha(100)
mistrect.fill(WHITE)

fpsClock    = pygame.time.Clock()
FPS         = 30

G           = -6
JUMPSPEED   = 50
PLAYERSPEED = 10
PLAYERRUSHBONUS= 20
PLAYERHEALTH= 500
PLAYERSATTACK=20
PLAYERREGEN = 5
PLAYERMASS  = 5

ENEMYSPEED  = 7
ENEMYJUMPSPD= 70
JUMPHEIGHT  = - ENEMYJUMPSPD ** 2 / (G * 2)
UPTIME      = - ENEMYJUMPSPD / G

pATTACK     = 0
pJUMP       = 1
pNOMAL      = 2
#           uuid, priority
IDLE        = [0, pNOMAL]
MOVING      = [1, pNOMAL]
JUMPUP      = [2, pJUMP]
JUMPDOWN    = [3, pJUMP]
ATTACK      = [4, pATTACK]

IDLEINTERVAL= 0.2
MOVEINTERVAL= 0.08
ATTACKINTERVAL = 0.02
NOINTERVAL  = 0
INVINCIBILITYINTERVAL = 0.08

INVINCIBILITYTIME = 0.7

wDAMAGEBOX  = 96

k_left      = K_a
k_right     = K_d
k_down      = K_s
k_jump      = K_k
k_rush      = K_l
k_attack    = K_j
k_pause     = K_p

list_platform= []
type_enemy  = []
list_enemy  = []
list_player = []
playerStandOn = []

score = [0]

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
    def show(self, color = RED, alpha = 128):
        rect = pygame.Surface((self.w, self.h))
        rect.set_alpha(alpha)
        rect.fill(color)
        mainsurf.blit(rect, (self.x, self.drawy))

class MovableObj:
    def __init__(self):
        # facing: 0 for left, 1 for right
        self.facing = 0
        self.attacking = 0
        self.state = IDLE
        self.standOn = 0
        self.onground = 1
        self.jumptimes = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
    def fallingDetection(self):
        if self.box.y + self.vy - G <= base:
            self.box.y = base
            self.landing()
            if self.attacking:
                self.damagebox.y = base
            return 0
        for i in list_platform:
            if self.box.x < i.rect_r and self.box.xr > i.rect_l:
                if i.rect_t <= self.box.y and i.rect_t > self.box.y + self.vy + G:
                    self.box.y = i.rect_t
                    if self.attacking:
                        self.damagebox.y = i.rect_t
                    self.landing()
                    return i.index
        self.onground = 0
        self.ay = G
        self.vy += self.ay
        return -1
    def jump(self):
        if  self.jumptimes < 2:
            self.vy = JUMPSPEED
            self.jumptimes += 1
            self.shiftState(JUMPUP)
    def jumpdown(self):
        if self.onground == 1 and self.box.y > base:
            self.box.y -= 1
            self.shiftState(JUMPDOWN)
    def landing(self):
        if self.onground == 0:
            self.onground = 1
            self.jumptimes = 0
            self.vy = 0
            self.ay = 0
            self.shiftState(IDLE, pJUMP)

    def shiftState(self, state, piority = 10):
        if state[0] != self.state[0] and (state[1] <= self.state[1] or self.state[1] >= piority):
            self.picindex = 0
            self.state = state

class StillObj:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.coord()
    def coord(self):
        self.w, self.h = self.img.get_size()
        self.drawy = HEIGHT - self.y - self.h
    def draw(self):
        mainsurf.blit(self.img, (self.x, self.drawy))

def clip(v, vmax):
    if v > vmax:
        return vmax
    elif v < -vmax:
        return -vmax
    return v
def chip(n, val):
    if n == 0:
        return 0
    if n > 0:
        if n < val:
            return 0
        else :
            return n - val
    else:
        if n > -val:
            return 0
        else :
            return n+ val
    pass
