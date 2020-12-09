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
        self.box.setPosition(x, y)
        MovableObj.__init__(self)
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state[0]][self.picindex], (self.box.x, self.box.drawy))

class PainBox(Enemy):
    def __init__(self, pic, damage, x, y):
        Enemy.__init__(self, pic, x, y)
        self.damage = damage
        self.attacking = 1
    def takeDamage(self):
        pass
    def causeDamage(self, playerbox):
        if self.box.isCollideWith(playerbox):
            return self.damage
        return 0
    def update(self):
        pass

painbox_sources_left = [[pygame.image.load('./resources/graphicals/painbox.png')],
                        [pygame.image.load('./resources/graphicals/painbox_hurt.png')]]
painbox_sources = [painbox_sources_left]

list_enemy.append(PainBox(painbox_sources, 15, 200, 400))
