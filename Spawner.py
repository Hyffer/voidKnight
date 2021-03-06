import pygame, time, random, math
from pygame.locals import *

from basis import *
from Enemy import *

m_challenge = 0
m_endless   = 1

MAXENEMYNUM = 5
sIDLE       = 0
sOPEN       = 1
sCLOSE      = -1
sNOSPAWN    = 0
sSPAWNING   = 1
sSPAWNED    = 2

PAUSEPREOPEN        = 8
PAUSEPRESPAWN       = 5
PAUSEPOSTSPAWN      = 6
PAUSEBETWEENSPAWN   = 85
PAUSEBETWEENSPAWN_ENDLESS= 15

# out of 0 - 99
GHOULUPPER  = 50
BALLUPPER   = 88
MONKUPPER   = 100

class Spawner(StillObj):
    def __init__(self, pics, x, y):
        StillObj.__init__(self, pics[0], x, y)
        self.centerx = self.x + self.w/2
        self.pics = pics

        self.index = 0
        self.piclen = len(self.pics)
        self.enemylist = []
        # time and event control
        self.interval = 0.1
        self.lastTime = 0
        self.buf = 0
        # 0 for no spawn, 1 for spawning, 2 for spawned
        self.spawning = sNOSPAWN
        # 0 for no animation, 1 for open, -1 for close
        self.state = sIDLE
        self.lock = 0

    def update(self, mode):
        t = time.time()
        if (t - self.lastTime) <= self.interval:
            return
        else:
            self.lastTime = t
            if self.buf:
                self.buf -=1
                return
        # spawn and wait
        if self.spawning == sSPAWNING:
            for enemy in self.enemylist:
                list_enemy.append(enemy)
            self.enemylist = []
            self.spawning = sSPAWNED
            self.buf = PAUSEPOSTSPAWN
            self.state = sCLOSE
            if mode == m_challenge:
                score[1] += 1
            return
        # wait till spawn
        if self.index == self.piclen - 1 and self.spawning == sNOSPAWN:
            self.buf = PAUSEPRESPAWN
            self.spawning = sSPAWNING
        # gate open
        if self.state == sOPEN and self.index < self.piclen-1:
            self.index += 1
        #check for spawn
        if mode == m_challenge:
            self.checkSpawn()
        elif mode == m_endless:
            self.checkSpawn_endless()
        # gate close
        if self.state == sCLOSE and self.index > 0:
            self.index -= 1
            if self.index == 0:
                self.state = sIDLE
                if mode == m_challenge:
                    self.buf = PAUSEBETWEENSPAWN
                elif mode == m_endless:
                    self.buf = PAUSEBETWEENSPAWN_ENDLESS
                self.lock = False
        
        self.img = self.pics[self.index]

    def getEnemy(self, ratiolock = 0):
        r = random.randint(0, 2)
        largeratio = math.log2(score[0])/20 + 1 if (score[0] and not ratiolock) else 1
        if r == 0:
            return Ghoul(self.centerx + random.randint(-3, 3) * 10, self.y, 100, 50, enlarge = largeratio + 0.5)
        elif r == 1:
            return PainBall(self.centerx + random.randint(-3, 3) * 10, self.y, 60, 70, enlarge = largeratio)
        elif r == 2:
            return Monk(self.centerx + random.randint(-3, 3) * 10, self.y, enlarge = largeratio + 1)

    def getEnemy_endless(self):
        r = random.randint(0, 100)

        if r <= GHOULUPPER:
            hp, damage, speed, mass, knockback, enlarge = ghoulcalc(score[0])
            return Ghoul(self.centerx + random.randint(-3, 3) * 10, self.y, hp, damage, maxvx = speed , mass = mass, knockback = knockback,enlarge = enlarge)
        elif r <= BALLUPPER:
            hp, damage, speed , mass, knockback, enlarge= ballcalc(score[0])
            return PainBall(self.centerx + random.randint(-3, 3) * 10, self.y, hp, damage, maxvx = speed , mass = mass, knockback = knockback, enlarge = enlarge)
        elif r <= MONKUPPER:
            hp, damage, speed , mass, knockback, enlarge= monkcalc(score[0])
            return Monk(self.centerx + random.randint(-3, 3) * 10, self.y, hp, damage, maxvx = speed , mass = mass, knockback = knockback, enlarge = enlarge)

    def checkSpawn(self):
        if self.lock:
            return
        spawnnum = random.randint(3, MAXENEMYNUM)
        if spawnnum:
            self.lock = True
            for i in range(spawnnum):
                self.enemylist.append(self.getEnemy(1))
            self.state = sOPEN
            self.spawning = sNOSPAWN
            self.buf = PAUSEPREOPEN
            return
    def checkSpawn_endless(self):
        if self.lock:
            return
        spawnnum = random.randint(0, MAXENEMYNUM - len(list_enemy))
        if spawnnum:
            self.lock = True
            for i in range(spawnnum):
                self.enemylist.append(self.getEnemy_endless())
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

# returns hp, damage, speed, mass, knockback, enlarge
def ghoulcalc(x):
    largeratio = math.log2(score[0]) / 20 + 1 if score[0] else 1
    return GHOULHP0 + x * ENEMYHP_K, GHOULATTACK0 + x* ENEMYATTACK_K, GHOULSPEED0 + x * ENEMYSPEED_K * 0.7, GHOULMASS0 * largeratio, GHOULKNOCKBACK0 * largeratio, largeratio + 0.5
def ballcalc(x):
    largeratio = math.log2(score[0]) / 20 + 1 if score[0] else 1
    return BALLHP0 + x * ENEMYHP_K, BALLATTACK0 + x * ENEMYATTACK_K, BALLSPEED0 + x * ENEMYSPEED_K, BALLMASS0 * largeratio, BALLKNOCKBACK0 * largeratio, largeratio
def monkcalc(x):
    largeratio = math.log2(score[0]) / 20 + 1 if score[0] else 1
    return MONKHP0 + x * ENEMYHP_K, MONKATTACK0 + x * ENEMYATTACK_K, MONKSPEED0 + x * ENEMYSPEED_K * 0.5, MONKMASS0 * largeratio, MONKKNOCKBACK0 * largeratio, largeratio + 1