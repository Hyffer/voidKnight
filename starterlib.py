from typing import List, Any

import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()

WINWIDTH    = 768
WINHEIGHT   = 512
WINHALFWIDTH= WINWIDTH/2
WINHALFHEIGHT=WINHEIGHT/2

WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (255, 0, 0)

BASICFONT   = pygame.font.Font('freesansbold.ttf', 32)

mainsurf    = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)

fpsClock    = pygame.time.Clock()
FPS         = 30

G           = -10
PLAYERSPEED = 10

IDLE        = 0
MOVING      = 1
INTERVALIDLE= 0.5
INTERVALMOVE= 0.1
TIMENOHURT  = 3

list_madness= []
list_noMove = []
list_player = []
list_enemy  = []

class gameObj:  #x, y are coords of midbottom
    x = None
    y = None

class moveables(gameObj):
    hp = None
    vx = 0
    vy = 0
    ay = 0
    no_support = None
    facing = 1              #0 for left, 1 for right
    nowImg = [0, 0]         #0 for idle, 1 for moving
    imgs_r = [[]]
    imgs_l = [[]]
    imgs = None

class player(moveables):
    interval_idle = INTERVALIDLE
    interval_move = INTERVALMOVE
    lastIdleTime = 0
    lastMoveTime = 0
    no_hurt = False
    time_no_hurt = TIMENOHURT
    lastNoHurtTime = 0
    def __init__(self, imgs_r, imgs_l, coords):
        self.imgs_r = imgs_r
        self.imgs_l = imgs_l
        self.x, self.y = coords
    def animate(self):
        if self.facing:
            self.imgs = self.imgs_r
        else :
            self.imgs = self.imgs_l
        self.x += self.vx
        self.y += self.vy
        imgNum = len(self.imgs[self.nowImg[0]])
        if self.nowImg[0] == IDLE and time.time() - self.lastIdleTime > self.interval_idle:
            self.nowImg[1] = (self.nowImg[1] + 1) % imgNum
            self.lastIdleTime = time.time()
        if self.nowImg[0] == MOVING and time.time() - self.lastMoveTime > self.interval_move:
            self.nowImg[1] = (self.nowImg[1] + 1) % imgNum
            self.lastMoveTime = time.time()
    def coordsTranslate(self):
        a, b = self.imgs[self.nowImg[0]][self.nowImg[1]].get_size()
        return (self.x - a/2, WINHEIGHT - (self.y + b))
    def draw(self):
        mainsurf.blit(self.imgs[self.nowImg[0]][self.nowImg[1]], self.coordsTranslate())

class enemy(moveables):
    pass

class noMove(gameObj):
    img = None
    solid = None
    def __init__(self, img, coords, solid):
        self.x, self.y = coords
        self.img = img
        self.solid = solid
    def coordsTranslate(self):
        a, b = self.img.get_size()
        return (self.x - a/2, WINHEIGHT - (self.y + b))
    def draw(self):
        mainsurf.blit(self.img, self.coordsTranslate())

def playerEventHandle(player):
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.vx = PLAYERSPEED
                if not player.facing:
                    player.facing = 1
                player.nowImg[0] = MOVING
            if event.key == K_LEFT:
                player.vx = -PLAYERSPEED
                if player.facing:
                    player.facing = 0
                player.nowImg[0] = MOVING      #sets mode to moving. may make bug.
            if event.key == K_UP:
                pass
            if event.key == K_DOWN:
                pass
        elif event.type == KEYUP:       #sets speed to 0 when key is up. need update.
            if event.key == K_RIGHT:
                player.vx = 0
                if player.nowImg[0] == MOVING:
                    player.nowImg[0] = IDLE
            if event.key == K_LEFT:
                player.vx = 0
                if player.nowImg[0] == MOVING:
                    player.nowImg[0] = IDLE
            if event.key == K_UP:
                pass
            if event.key == K_DOWN:
                pass

def redraw():
    for i in list_noMove:
        i.draw()

def makeText(msg, clr, x, y):
    textsurf = BASICFONT.render(msg, True, clr)
    textrect = textsurf.get_rect()
    textrect.center = (x, y)
    return textsurf, textrect

def checkforquit():
    for evt in pygame.event.get():
        if evt.type == QUIT:
            terminate()

def terminate():
    pygame.quit()
    sys.exit()