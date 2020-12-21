import pygame, time
from pygame.locals import *

from basis import *
from Spawner import *
from EnemyVirtualInput import *

class Enemy(MovableObj, EnemyVI):
    def __init__(self, pic, damage, x, y):
        # picture init
        self.pic = pic
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        self.onground = 1
        self.attacking = 0
        self.damage = damage
        # collision box init
        w, h = pic[0][0][0].get_size()
        self.box = Box(w, h)
        self.damagebox = Box(w, h)
        self.initx = x
        self.inity = y
        self.build()
        MovableObj.__init__(self)
    def build(self):
        self.box.setPosition(self.initx, self.inity)
        self.damagebox.setPosition(self.initx, self.inity)
    def takeDamage(self, damage):
        pass
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state[0]][self.picindex], (self.box.x, self.box.drawy))
        if self.attacking:
            self.damagebox.show()

    def update(self):
        self.vx = ENEMYSPEED * self.track()
        
        fdreturn = self.fallingDetection()
        if fdreturn != -1:
            self.standOn = fdreturn
        
        self.box.moving(self.vx, self.vy)
        self.damagebox.moving(self.vx, self.vy)

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


ghoul_sorces_left = [[pygame.image.load('./resources/graphicals/ghoul/ghoul_001.png'),
                      pygame.image.load('./resources/graphicals/ghoul/ghoul_002.png'),
                      pygame.image.load('./resources/graphicals/ghoul/ghoul_003.png'),
                      pygame.image.load('./resources/graphicals/ghoul/ghoul_004.png'),
                      pygame.image.load('./resources/graphicals/ghoul/ghoul_005.png'),
                      pygame.image.load('./resources/graphicals/ghoul/ghoul_006.png'),
                      pygame.image.load('./resources/graphicals/ghoul/ghoul_007.png'),
                      pygame.image.load('./resources/graphicals/ghoul/ghoul_008.png')]]

class Ghoul(Enemy):
    def __init__(self, pic, damage, x, y):
        Enemy.__init__(self, pic, damage, x, y)
        self.interval = 0.2
        self.lastTime = 0

    def update(self):
        distx = self.track()
        if distx > 0:
            self.facing = 1
        elif distx < 0:
            self.facing = 0

        self.vx = ENEMYSPEED * self.track()

        fdreturn = self.fallingDetection()
        if fdreturn != -1:
            self.standOn = fdreturn

        self.box.moving(self.vx, self.vy)
        self.damagebox.moving(self.vx, self.vy)

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
    def __init__(self, pic, damage, x, y, _ax = 2, maxvx = 15):
        Enemy.__init__(self, pic, damage, x, y)
        self._ax = _ax
        self.maxvx = maxvx
        self.interval = [0.05]
        self.lastTime = [0]

    def update(self):
        distx = self.track()
        if distx > 0:
            self.facing = 1
            self.ax = self._ax
        elif distx < 0:
            self.facing = 0
            self.ax = -self._ax

        self.vx = accelerate(self.vx, self.ax, self.maxvx)

        fdreturn = self.fallingDetection()
        if fdreturn != -1:
            self.standOn = fdreturn
        
        self.box.moving(self.vx, self.vy)
        self.damagebox.moving(self.vx, self.vy)


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

#enemySquare = movingEnemy(movingenemy_sources, 15, 200, 400)
enemyBall = PainBall(painball_sources, 15, 0, base)
ghoul = Ghoul(ghoul_sources, 25, 0, base)
gate.spawn([enemyBall, ghoul])


'''
class PainBox(Enemy):
    def __init__(self, pic, damage, x, y):
        Enemy.__init__(self, pic, x, y)
        self.damage = damage
        self.attacking = 1
    def takeDamage(self):
        pass
    def causeDamage(self, list_player[0]box):
        if self.box.isCollideWith(list_player[0]box):
            return self.damage
        return 0
    def update(self, list_player[0]box):
        pass
'''
