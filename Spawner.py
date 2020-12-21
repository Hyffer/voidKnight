import pygame, time, random
from pygame.locals import *

from basis import *
from Enemy import *

MAXENEMYNUM = 10
sIDLE       = 0
sOPEN       = 1
sCLOSE      = -1

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
        self.spawning = False
        # 0 for no animation, 1 for open, -1 for close
        self.state = sIDLE
        self.lock = 0
    def firstSpawn(self):
        self.spawn()
        t = time.time()
        self.lastTime = t - self.interval + 0.5
    def update(self):
        t = time.time()
#        tick = (t - self.lastTime) > self.interval
#        if not tick:
#            return
#        # wait buf
#        if self.buf >0:
#            self.buf -= 1
#            self.lastTime = t
#            return

        if (t - self.lastTime) <= self.interval:
            return
        else:
            self.lastTime = t
            self.spawn()
#        '''# gate open
#        if self.state == 1 and self.index < self.piclen:
#            self.index +=1
#        # gate close
#        if self.state == -1 and self.index >= 0:
#            self.index -= 1
#        if self.state ==-1 and self.index ==0:
#            self.state = 0
#        # wait till spawn
#        if self.index == self.piclen - 1 and self.spawning == 0:
#            self.buf = 2
#            self.spawning = True
#
        # spawn and wait
        if self.spawning == True:
            for enemy in self.enemylist:
                enemy.box.setPosition(self.centerx, self.y)
                enemy.damagebox.setPosition(self.centerx, self.y)
                list_enemy.append(enemy)
            self.spawning = Fasle
            self.buf = 2
            self.state = sCLOSE
            return
        # wait till spawn
        if self.index == self.piclen - 1 and self.spawning == False:
            self.buf = 2
            self.spawning = True
        # gate open
        if self.state == sOPEN and self.index < self.piclen-1:
            self.index += 1
        # gate close
        if self.state == sCLOSE and self.index >= 0:
            self.index -= 1
        if self.state == sCLOSE and self.index == 0:
            self.state = sIDLE
        self.img = self.pics[self.index]
        self.lastTime = t

#    def spawn(self, enemylist):
#        self.buf = 2
#        self.state = 1
#        self.enemylist = enemylist
    def spawn(self):
        addEnemy(random.randint(0, 1), self.centerx, self.y)
    def checkSpawn(self):
        

gate_resources = [pygame.image.load('./resources/graphicals/spawner_gate/gate_000.png'),
                  pygame.image.load('./resources/graphicals/spawner_gate/gate_001.png')]
gate = Spawner(gate_resources, 800, base)
