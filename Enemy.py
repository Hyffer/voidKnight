import pygame, time
from pygame.locals import *

from Player import player
from basis import *

class Enemy(MovableObj):
    #init pic, x, y
    def __init__(self, pic, x, y):
        # picture init
        self.pic = pic
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        # collision box init
        w, h = pic[0][0][0].get_size()
        self.box = Box(w, h)
        self.initx = x
        self.inity = y
        self.build()
        self.damagebox = Box(0, 0)
        MovableObj.__init__(self)
    def build(self):
        self.box.setPosition(self.initx, self.inity)
    def takeDamage(self, damage):
        pass
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state[0]][self.picindex], (self.box.x, self.box.drawy))
        if self.attacking:
            self.damagebox.show()

class movingEnemy(Enemy):
    def __init__(self, pic, damage, x, y):
        Enemy.__init__(self, pic, x, y)
        self.damage = damage
        self.onground = 1
        self.damagebox = Box(self.box.w, self.box.h)
        self.damagebox.setPosition(self.box.centerx, self.box.y)
        self.attacking = 1

    def track(self):
        # follow palyer
        # -1 for left, 1 for right, 0 for stop
        
        # at the same stage
        if self.standOn == list_player[0].standOn:
            if self.box.x >= list_player[0].box.xr:
                return -1
            elif self.box.xr <= list_player[0].box.x:
                return 1
            return 0
        else:
            goto = list_platform[self.standOn].route[list_player[0].standOn]
            # overlap
            if list_platform[self.standOn].rect_l <= list_platform[goto].rect_r and list_platform[self.standOn].rect_r >= list_platform[goto].rect_l:
                if self.box.centerx < list_platform[goto].rect_l:
                    return 1
                elif self.box.centerx > list_platform[goto].rect_r:
                    return -1
                else :
                    if list_platform[self.standOn].rect_t >= list_platform[goto].rect_t:
                        self.jumpdown()
                    elif list_platform[self.standOn].rect_t < list_platform[goto].rect_t:
                        self.jump()
                    return 0
            # towards left
            elif list_platform[self.standOn].rect_l > list_platform[goto].rect_r:
                if self.box.centerx <= list_platform[self.standOn].rect_l:
                    self.jump()
                if self.box.centerx <= list_platform[goto].rect_l:
                    return 0
                return 1
            # towards right
            elif list_platform[self.standOn].rect_r < list_platform[goto].rect_l:
                if self.box.centerx >= list_platform[self.standOn].rect_r:
                    self.jump()
                if self.box.centerx >= list_platform[goto].rect_l:
                    return 0
                return 1
            return 0

    def update(self):
        self.vx = ENEMYSPEED * self.track()
        
        fdreturn = self.fallingDetection()
        if fdreturn != -1:
            self.standOn = fdreturn
        
        self.box.moving(self.vx, self.vy)
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


class PainBall(movingEnemy):
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

    def update(self):
        distx = self.track()
        if distx > 0:
            self.facing = 1
            self.ax = self.maxax
        if distx <0:
            self.facing = 0
            self.ax = -self.maxax

        self.vx += self.ax
        self.vx = clip(self.vx, self.maxvx)

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

list_enemy.append(movingEnemy(movingenemy_sources, 15, 200, 400))
list_enemy.append(PainBall(painball_sources, 15, 0, base))


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
