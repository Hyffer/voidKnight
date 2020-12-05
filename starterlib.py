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

#BASICFONT   = pygame.font.Font('freesansbold.ttf', 32)

mainsurf    = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

fpsClock    = pygame.time.Clock()
FPS         = 30

G           = -6
JUMPSPEED   = 50
PLAYERSPEED = 10

IDLE        = 0
MOVING      = 1

IDLEINTERVAL= 0.8
MOVEINTERVAL= 0.1

list_madness= []
list_platform= []
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

class Platform(StillObj):
    def __init__(self, img, x, y):
        StillObj.__init__(self, img, x, y)
        w, h = img.get_size()
        self.rect_t = y + h
        self.rect_l = x
        self.rect_r = x + w

platform_sources = [('./resources/graphicals/stage_bottom.png', (0, 0)),
                    ('./resources/graphicals/stage_top.png', (hWIDTH - 128, 64)),
                    ('./resources/graphicals/stage_left.png', (hWIDTH - 128 -32, 64)),
                    ('./resources/graphicals/stage_right.png', (hWIDTH + 128, 64)),
                    ('./resources/graphicals/platform_M.png', (hWIDTH, 500)),
                    ('./resources/graphicals/platform_L.png', (25, 300))]
for i, (x, y) in platform_sources:
    img = pygame.image.load(i)
    obj = Platform(img, x, y)
    list_platform.append(obj)

class MovableObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # state: 0 for idle, 1 for moving
        self.state = 0
        self.onground = 1
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        # facing: 0 for left, 1 for right
        self.facing = 1

class Player(MovableObj):
    def __init__(self, pic):
        self.pic = pic
        self.piclen = len(pic[0][0])
        self.picindex = 0
        self.interval = [IDLEINTERVAL, MOVEINTERVAL]
        self.lastTime = [0, 0]
        self.w, self.h = pic[0][0][0].get_size()
        MovableObj.__init__(self, hWIDTH - self.w/2, 128)
    def update(self, direction, jump):
        # collision box update
        self.rect_l = self.x
        self.rect_r = self.x + self.w
        
        # moving state update
        if direction == K_d and self.x + self.w < WIDTH:
            self.vx = PLAYERSPEED
            self.state = 1
            self.facing = 1
        elif direction == K_a and self.x > 0:
            self.vx = -PLAYERSPEED
            self.state = 1
            self.facing = 0
        else:
            self.vx = 0
            self.state = 0
        self.x += self.vx

        if jump == 1 and self.leaveground < 2:
            self.vy = JUMPSPEED
            self.leaveground += 1
        if jump == -1 and self.leaveground == 0:
            self.y -= 2

        # falling update
        collideDetect(self)
        self.y += self.vy
        if self.y < base:
            self.y = base
        
        # pic update
        t = time.time()
        if(t - self.lastTime[self.state] > self.interval[self.state]):
            self.picindex = (self.picindex + 1) % self.piclen
            self.lastTime[self.state] = t
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state][self.picindex], (self.x, HEIGHT - self.y - self.h))

class Enemy(MovableObj):
    def __init__(self, pic):
        self.pic = pic

def collideDetect(movable):
    for i in list_platform:
        if movable.rect_l < i.rect_r and movable.rect_r > i.rect_l:
            if i.rect_t - 1 <= movable.y and i.rect_t > movable.y + movable.vy - 10:
                movable.vy = 0
                movable.ay = 0
                movable.y = i.rect_t
                movable.leaveground = 0
                return
    movable.ay = G
    movable.vy += movable.ay
    movable.onground = 0

