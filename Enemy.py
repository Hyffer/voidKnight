import pygame
from pygame.locals import *
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
        self.initx = x
        self.inity = y
        self.build()
        MovableObj.__init__(self)
    def build(self):
        self.box.setPosition(self.initx, self.inity)
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state[0]][self.picindex], (self.box.x, self.box.drawy))

class movingEnemy(Enemy):
    def __init__(self, pic, damage, x, y):
        Enemy.__init__(self, pic, x, y)
        self.damage = damage
        self.onground = 1
        self.attacking = 1
    def takeDamage(self):
        pass
    def causeDamage(self, playerbox):
        if self.box.isCollideWith(list_player[0].box):
            return self.damage
        return 0
    def update(self):
        # follow palyer
        # at the same stage
        if self.standOn == list_player[0].standOn:
            if self.box.x >= list_player[0].box.xr:
                self.vx = -ENEMYSPEED
            elif self.box.xr <= list_player[0].box.x:
                self.vx = ENEMYSPEED
                    
        else:
            goto = list_platform[self.standOn].route[list_player[0].standOn]
            # overlap
            if list_platform[self.standOn].rect_l <= list_platform[goto].rect_r and list_platform[self.standOn].rect_r >= list_platform[goto].rect_l:
                if self.box.centerx < list_platform[goto].rect_l:
                    self.vx = ENEMYSPEED
                elif self.box.centerx > list_platform[goto].rect_r:
                    self.vx = -ENEMYSPEED
                else :
                    self.vx = 0
                    if list_platform[self.standOn].rect_t >= list_platform[goto].rect_t:
                        self.jumpdown()
                    elif list_platform[self.standOn].rect_t < list_platform[goto].rect_t:
                        self.jump()
            # towards left
            elif list_platform[self.standOn].rect_l > list_platform[goto].rect_r:
                self.vx = -ENEMYSPEED
                if self.box.centerx <= list_platform[self.standOn].rect_l:
                    self.jump()
                if self.box.centerx <= list_platform[goto].rect_l:
                    self.vx = 0
            # towards right
            elif list_platform[self.standOn].rect_r < list_platform[goto].rect_l:
                self.vx = ENEMYSPEED
                if self.box.centerx >= list_platform[self.standOn].rect_r:
                    self.jump()
                if self.box.centerx >= list_platform[goto].rect_l:
                    self.vx = 0

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

list_enemy.append(movingEnemy(movingenemy_sources, 15, 200, 400))

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

painbox_sources_left = [[pygame.image.load('./resources/graphicals/painbox.png')],
                        [pygame.image.load('./resources/graphicals/painbox_hurt.png')]]
painbox_sources = [painbox_sources_left]

list_enemy.append(PainBox(painbox_sources, 15, 200, 400))
'''
