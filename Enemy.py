import pygame
from pygame.locals import *
from basis import *

class Enemy(MovableObj):
    id = None
    #sets pics only
    def __init__(self, pic, x, y):
        MovableObj.__init__(self, pic, x, y)
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
        if self.box.collidebox(playerbox):
            return self.damage
        return 0
    def update(self):
        pass

painbox_sources_left = [[pygame.image.load('./resources/graphicals/painbox.png')],
                        [pygame.image.load('./resources/graphicals/painbox_hurt.png')]]
painbox_sources = [painbox_sources_left]

list_enemy.append(PainBox(painbox_sources, 15, 200, 400))
