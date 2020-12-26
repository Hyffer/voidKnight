import pygame, time, random 
from pygame.locals import *

from basis import *
from EnemyVirtualInput import *
from Sounds import *

class Enemy(MovableObj, EnemyVI):
    def __init__(self, pic, health, damage, knockback, mass, x, y, enlarge):
        # picture init
        if enlarge == 1:
            self.pic = pic
        else:
            self.pic = [[[pygame.transform.scale(i, (int(i.get_size()[0]*enlarge), int(i.get_size()[1]*enlarge))) for i in j] for j in k] for k in pic]
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        self.onground = 1
        self.HEALTH = health
        self.health = health
        self.damage = damage
        self.mass = mass
        # collision box init
        w, h = self.pic[0][0][0].get_size()
        self.invicibility = ATTACKINTERVAL* 4
        self.lastHit = 0
        self.box = Box(w, h)
        self.damagebox = Box(w, h)
        self.healthbar = pygame.Surface((self.health*0.7, 5))
        self.healthbar.fill(GREEN)
        self.initx = x
        self.inity = y
        self.knockback = knockback
        self.knockbackvx = 0
        self.build()
        MovableObj.__init__(self)
        self.attacking = 1
    def build(self):
        self.box.setPosition(self.initx, self.inity)
        #self.damagebox.setPosition(self.initx, self.inity)
    def takeDamage(self, towards ,damage, knockback):
        t = time.time()
        if t - self.lastHit < self.invicibility:
            return 0
        self.lastHit = t
        self.health -= damage
        if self.health <= 0:
            list_enemy.remove(self)
            random.choice(sounds_monsterdeath).play()
            score[0] += 1
            return 1
        random.choice(sounds_hit).play()
        self.healthbar = pygame.Surface((self.health*0.7, 5))
        # healthbar
        if self.health < self.HEALTH*0.2:
            self.healthbar.fill(RED)
        else:
            self.healthbar.fill(GREEN)
        # movement
        self.knockbackvx = knockback *  (towards*2 - 1)
        #self.box.moving((towards*2-1) * (random.randint(80, 120)), 0)
        #self.vx = self.vx*0.4 + (towards*2-1)*self.vx*0.6
        self.vy = knockback /2
        return 1
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state[0]][self.picindex], (self.box.x, self.box.drawy))
        mainsurf.blit(self.healthbar, (self.box.x, self.box.drawy-15))


# @Override
    def jump(self):
        if self.onground == 1:
            self.vy = ENEMYJUMPSPD
            self.ay = G
    def jumpdown(self):
        if self.onground == 1 and self.box.y > base:
            self.box.y -= 1
    def landing(self):
        if self.onground == 0:
            self.onground = 1
            self.vy = 0
            self.ay = 0
        
movingenemy_sources_left = [[pygame.image.load('./resources/graphicals/painbox.png')],
                            [pygame.image.load('./resources/graphicals/painbox_hurt.png')]]
movingenemy_sources = [movingenemy_sources_left]

class Ghoul(Enemy):
    def __init__(self, x, y, health = 200, damage = 50 , maxvx = 7, AX = 1, knockback = 20, mass = 5, enlarge = 1):
        Enemy.__init__(self, ghoul_sources, health, damage, knockback, mass, x, y, enlarge)
        self.maxvx = maxvx
        self.AX = AX
        self.interval = 0.2
        self.lastTime = 0

    def update(self):
        distx = self.track()
        if distx > 0:
            self.facing = 1
            self.ax = self.AX
        elif distx < 0:
            self.facing = 0
            self.ax = -self.AX

        self.vx += self.ax
        self.vx = clip(self.vx, self.maxvx)
        if self.knockbackvx != 0:
            self.vx += self.knockbackvx
            self.knockbackvx = chip(self.knockbackvx, self.mass)

        fdreturn = self.fallingDetection()
        if fdreturn != -1:
            self.standOn = fdreturn

        self.box.moving(self.vx, self.vy)
        #self.damagebox.moving(self.vx, self.vy)

        t = time.time()
        if t - self.lastTime > self.interval:
            self.lastTime = t
            self.picindex = (self.picindex + 1) % self.piclen[0]

ghoul_sources_left = [[
    pygame.image.load('./resources/graphicals/ghoul/ghoul_001.png'),
    pygame.image.load('./resources/graphicals/ghoul/ghoul_002.png'),
    pygame.image.load('./resources/graphicals/ghoul/ghoul_003.png'),
    pygame.image.load('./resources/graphicals/ghoul/ghoul_004.png'),
    pygame.image.load('./resources/graphicals/ghoul/ghoul_005.png'),
    pygame.image.load('./resources/graphicals/ghoul/ghoul_006.png'),
    pygame.image.load('./resources/graphicals/ghoul/ghoul_007.png'),
    pygame.image.load('./resources/graphicals/ghoul/ghoul_008.png'),
]]
ghoul_sources_right = [[pygame.transform.flip(i, True, False) for i in j] for j in ghoul_sources_left]
ghoul_sources = [ghoul_sources_left, ghoul_sources_right]

class PainBall(Enemy):
    def __init__(self, x, y, health, damage, AX = 2, maxvx = 15, knockback = 10, mass = 7, enlarge = 1):
        Enemy.__init__(self, painball_sources, health, damage, knockback, mass, x, y, enlarge)
        self.AX = AX
        self.maxvx = maxvx
        self.interval = [0.05]
        self.lastTime = [0]

    def update(self):
        distx = self.track()
        if distx > 0:
            self.facing = 1
            self.ax = self.AX
        elif distx < 0:
            self.facing = 0
            self.ax = -self.AX

        self.vx += self.ax
        self.vx = clip(self.vx, self.maxvx)
        if self.knockbackvx != 0:
            self.vx += self.knockbackvx
            self.knockbackvx = chip(self.knockbackvx, self.mass)

        fdreturn = self.fallingDetection()
        if fdreturn != -1:
            self.standOn = fdreturn
        
        self.box.moving(self.vx, self.vy)
        #self.damagebox.moving(self.vx, self.vy)


        t = time.time()
        if (t - self.lastTime[self.state[0]] > self.interval[self.state[0]]):
            self.picindex = (self.picindex + 1) % self.piclen[self.state[0]]
            self.lastTime[self.state[0]] = t


painball_sources_right = [[pygame.image.load('./resources/graphicals/painball/painball.001.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.002.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.003.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.004.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.005.png'),],]
painball_sources_left = [[pygame.transform.flip(i, True, False) for i in j] for j in painball_sources_right]
painball_sources = [painball_sources_left, painball_sources_right]

class monk(Enemy):
    pass
