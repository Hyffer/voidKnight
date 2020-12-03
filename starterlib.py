from typing import List, Any

import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()

<<<<<<< Updated upstream
WINWIDTH    = 768
WINHEIGHT   = 512
WINHALFWIDTH= WINWIDTH/2
WINHALFHEIGHT=WINHEIGHT/2
=======
WIDTH       = 1024
HEIGHT      = 768
hWIDTH      = WIDTH/2
>>>>>>> Stashed changes

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

IDLEINTERVAL= 0.8
MOVEINTERVAL= 0.1

list_madness= []
list_noMove = []
list_player = []
list_enemy  = []

<<<<<<< Updated upstream
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
=======
platform_sources = [pygame.image.load('./resources/graphicals/platform_M.png'),
                    pygame.image.load('./resources/graphicals/platform_L.png'),
                    pygame.image.load('./resources/graphicals/platform_XL.png')]

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
    def __init__(self, size, x, y):
        StillObj.__init__(self, platform_sources[size], x, y)

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
        self.interval = [IDLEINTERVAL, MOVEINTERVAL]
        self.lastTime = [0, 0]
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

        t = time.time()
        piclen = len(self.pic[self.facing][self.state])
        if(t - self.lastTime[self.state] > self.interval[self.state]):
            self.picindex = (self.picindex + 1) % piclen
            self.lastTime[self.state] = t
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state][self.picindex], (self.x, self.y))

class Enemy(MovableObj):
    def __init__(self, pic):
        self.pic = pic
>>>>>>> Stashed changes
