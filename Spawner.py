import pygame, time, random
from pygame.locals import *

from basis import *
from Enemy import *

MAXENEMYNUM = 5
sIDLE       = 0
sOPEN       = 1
sCLOSE      = -1
sNOSPAWN    = 0
sSPAWNING   = 1
sSPAWNED    = 2

PAUSEPREOPEN        = 2
PAUSEPRESPAWN       = 1
INTERVALSPAWN       = 1
PAUSEPOSTSPAWN      = 1
PAUSEBETWEENSPAWN   = 5

class Spawner(StillObj):
    def __init__(self, pics, x, y):
        StillObj.__init__(self, pics[0], x, y)
        self.centerx = self.x + self.w/2
        self.y = y
        self.pics = pics

        self.index = 0
        self.piclen = len(self.pics)
        self.enemylist = []
        # time and event control
        self.interval = 0.5
        self.lastTime = 0
        self.buf = 0
        # 0 for no spawn, 1 for spawning, 2 for spawned
        self.spawning = sNOSPAWN
        # 0 for no animation, 1 for open, -1 for close
        self.state = sIDLE
        self.lock = 0
    def firstSpawn(self):
        return
        self.spawn()
        t = time.time()
        self.lastTime = t - self.interval + 0.5
    def update(self):
        t = time.time()
#        tick = (t - self.lastTime) > self.interval
#        if not tick:
#            return
#        # wait buf
#

        if (t - self.lastTime) <= self.interval:
            return
        else:
            self.lastTime = t
            if self.buf:
                self.buf -=1
                return

#        # gate open
#        if self.state == sOPEN and self.index < self.piclen:
#            self.index += 1
#        # gate close
#        if self.state == sCLOSE and self.index >= 0:
#            self.index -= 1
#            if self.index ==0:
#                self.state = 0
#        # wait till spawn
#        if self.index == self.piclen - 1 and self.spawning == 0:
#            self.buf = 2
#            self.spawning = True
#
        # spawn and wait
        if self.spawning == sSPAWNING:
            for enemy in self.enemylist:
                list_enemy.append(enemy)
            self.enemylist = []
            self.spawning = sSPAWNED
            self.buf = PAUSEPOSTSPAWN
            self.state = sCLOSE
            return
        # wait till spawn
        if self.index == self.piclen - 1 and self.spawning == sNOSPAWN:
            self.buf = PAUSEPRESPAWN
            self.spawning = sSPAWNING
        # gate open
        if self.state == sOPEN and self.index < self.piclen-1:
            self.index += 1
        # gate close
        if self.state == sCLOSE and self.index > 0:
            self.index -= 1
            if self.index == 0:
                self.state = sIDLE
                self.buf = PAUSEBETWEENSPAWN
                self.lock = False
        self.checkSpawn()
        self.img = self.pics[self.index]

#    def spawn(self, enemylist):
#        self.buf = 2
#        self.state = 1
#        self.enemylist = enemylist
    def spawn(self):
        addEnemy(random.randint(0, 1), self.centerx, self.y)
    def getEnemy(self):
        return Ghoul(100, 50, self.centerx, self.y)
    def checkSpawn(self):
        if self.lock:
            return
        spawnnum = random.randint(0, MAXENEMYNUM - len(list_enemy))
        if spawnnum:
            self.lock = True
            for i in range(spawnnum):
                self.enemylist.append(self.getEnemy())
            self.state = sOPEN
            self.spawning = sNOSPAWN
            self.buf = PAUSEPREOPEN
            return
    def draw(self):
        mainsurf.blit(self.img, (self.x, self.drawy))
        if self.spawning == sSPAWNING or self.spawning == sNOSPAWN and (int((time.time())*5)%2):
            mainsurf.blit(warning_icon, (self.centerx - 25, self.drawy - 50))


gate_resources = [pygame.image.load('./resources/graphicals/spawner_gate/gate_000.png'),
                  pygame.image.load('./resources/graphicals/spawner_gate/gate_001.png')]
warning_icon = pygame.image.load('./resources/graphicals/icon/warning_alt.png')
gate = Spawner(gate_resources, 800, base)
