import pygame, time
from pygame.locals import *

from Player import player
from basis import *

class Enemy(MovableObj):
    def __init__(self, pic, x, y):
        # picture init
        self.pic = pic
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        # collision box init
        w, h = pic[0][0][0].get_size()
        self.box = Box(w, h)
        self.box.setPosition(x, y)
        self.damagebox = Box(0, 0)
        MovableObj.__init__(self)
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state[0]][self.picindex], (self.box.x, self.box.drawy))

class PainBox(Enemy):
    def __init__(self, pic, damage, x, y):
        Enemy.__init__(self, pic, x, y)
        self.damage = damage
        self.damagebox = Box(self.box.w, self.box.h)
        self.damagebox.setPosition(self.box.centerx, self.box.y)
        self.attacking = 1
    def takeDamage(self, damage):
        print('painbox is harmed by ', damage)
    def causeDamage(self, playerbox):
        if self.box.isCollideWith(playerbox):
            return self.damage
        return 0
    def update(self):
        pass

class PainBall(Enemy):
    def __init__(self, pic, damage, x, y, maxax = 2, maxvx = 15):
        Enemy.__init__(self, pic, x, y)
        self.maxax = maxax
        self.maxvx = maxvx
        self.damage = damage
        self.damagebox = Box(self.box.w, self.box.h)
        self.damagebox.setPosition(self.box.centerx, self.box.y)
        self.attacking = 1
        self.interval = [0.05]
        self.lastTime = [0]

    def takeDamage(self, damage):
        pass
    '''
    def causeDamage(self, playerbox):
        if self.box.isCollideWith(playerbox):
            return self.damage
        return 0
    '''
    def update(self):
        distx =  player.box.centerx - self.box.centerx
        if distx > 0:
            self.facing = 1
            self.ax = self.maxax
        if distx <0:
            self.facing = 0
            self.ax = -self.maxax

        self.vx += self.ax
        self.vx = clip(self.vx, self.maxvx)

        self.box.moving(self.vx, self.vy)
        self.damagebox.moving(self.vx, self.vy)

        t = time.time()
        if (t - self.lastTime[self.state[0]] > self.interval[self.state[0]]):
            self.picindex = (self.picindex + 1) % self.piclen[self.state[0]]
            self.lastTime[self.state[0]] = t



painbox_sources_left = [[pygame.image.load('./resources/graphicals/painbox.png')],
                        [pygame.image.load('./resources/graphicals/painbox_hurt.png')]]
painbox_sources = [painbox_sources_left]

painball_sources_left = [[pygame.image.load('./resources/graphicals/painball/painball.001.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.002.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.003.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.004.png'),
                            pygame.image.load('./resources/graphicals/painball/painball.005.png'),],]
painball_sources = [[[pygame.transform.flip(i, True, False) for i in j] for j in painball_sources_left], painball_sources_left,]

list_enemy.append(PainBox(painbox_sources, 15, 200, 400))
list_enemy.append(PainBall(painball_sources, 15, 400, base))
