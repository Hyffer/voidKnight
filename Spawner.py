import pygame, time
from pygame.locals import *
from Player import player
from basis import *

class Spawner(StillObj):
    def __init__(self, pics, x, y):
        StillObj.__init__(self, pics[0], x, y)
        self.centerx = self.x + self.w/2
        self.pics = pics
        self.interval = 1
        self.buf = 0
        self.lastTime = 0
        self.index = 0
        self.piclen = len(self.pics)
        self.enemylist = None
        self.event = 0
        # 0 for no animation, 1 for open, -1 for close
        self.state = 0
    def update(self):
        if self.state == 0:
            return
        t = time.time()
        tick = (t - self.lastTime) > self.interval
        if not tick:
            return
        # wait buf
        if self.buf >0:
            self.buf -= 1
            self.lastTime = t
            return

        # spawn and wait
        if self.event == 1:
            for enemy in self.enemylist:
                enemy.box.setPosition(self.centerx, self.y)
                enemy.damagebox.setPosition(self.centerx, self.y)
                list_enemy.append(enemy)
            self.event = 0
            self.buf = 2
            self.state = -1
            return
        # wait till spawn
        if self.index == self.piclen - 1 and self.event == 0:
            self.buf = 2
            self.event = 1
        # gate open
        if self.state == 1 and self.index < self.piclen-1:
            self.index += 1
        # gate close
        if self.state == -1 and self.index >= 0:
            self.index -= 1
        if self.state == -1 and self.index == 0:
            self.state = 0
        self.img = self.pics[self.index]
        self.lastTime = t

    def spawn(self, enemylist):
        self.buf = 2
        self.state = 1
        self.enemylist = enemylist

gate_resources = [pygame.image.load('./resources/graphicals/spawner_gate/gate_000.png'),
                  pygame.image.load('./resources/graphicals/spawner_gate/gate_001.png')]
gate = Spawner(gate_resources, 800, base)
