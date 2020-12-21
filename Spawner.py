import pygame, time, random
from pygame.locals import *

from basis import *
from Enemy import *


def addEnemy(i, x, y):
    if i == 0:
        list_enemy.append(PainBall(painball_sources, 80, 15, x, y))
    elif i == 1:
        list_enemy.append(Enemy(movingenemy_sources, 140, 15, x, y))

class Spawner(StillObj):
    def __init__(self, pics, x, y):
        StillObj.__init__(self, pics[0], x, y)
        self.centerx = self.x + self.w/2
        self.y = y
        self.pics = pics
        self.interval = 5
        self.lastTime = 0
        self.index = 0
        self.piclen = len(self.pics)
        self.enemylist = []
        self.event = 0
        # 0 for no animation, 1 for open, -1 for close
        self.state = 0
    def firstSpawn(self):
        self.spawn()
        t = time.time()
        self.lastTime = t - self.interval + 0.5
    def update(self):
        t = time.time()
        if (t - self.lastTime) <= self.interval:
            return
        else:
            self.lastTime = t
            self.spawn()
        '''# gate open
        if self.state == 1 and self.index < self.piclen:
            self.index +=1
        # gate close
        if self.state == -1 and self.index >= 0:
            self.index -= 1
        if self.state ==-1 and self.index ==0:
            self.state = 0
        # wait till spawn
        if self.index == self.piclen - 1 and self.event == 0:
            self.buf = 2
            self.event = 1
        # spawn and wait
        if self.event == 1:
            for enemy in self.enemylist:
                enemy.box.setPosition(self.centerx, self.y)
                enemy.damagebox.setPosition(self.centerx, self.y)
                list_enemy.append(enemy)
            self.event = 0
            self.buf = 2
            self.state = -1
        self.img = self.pics[self.index]
        self.lastTime = t'''
    def spawn(self):
        addEnemy(random.randint(0, 1), self.centerx, self.y)

gate_resources = [pygame.image.load('./resources/graphicals/spawner_gate/gate_000.png'),
                  pygame.image.load('./resources/graphicals/spawner_gate/gate_001.png')]
gate = Spawner(gate_resources, 800, base)
