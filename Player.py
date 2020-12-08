import pygame, time
from pygame.locals import *
from basis import *

class Player(MovableObj):
    def __init__(self, pic, initx, inity):
        MovableObj.__init__(self, pic, initx, inity)
        self.lastTime = [0, 0, 0, 0, 0]
        self.interval = [IDLEINTERVAL, MOVEINTERVAL, NOINTERVAL, NOINTERVAL, ATTACKINTERVAL]
        self.health = 500
    def rebuild(self):
        self.health = 500
        self.facing = 0
        self.attacking = 0
        self.state = IDLE
        self.onground = 1
        self.jumptimes = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.box.x = initx - self.box.w/2
        self.box.y = inity
        self.box.boxUpdate()
        
    def update(self, direction, rush, jump, attack):
        # moving state update
        # y
        if jump == 1 and self.jumptimes < 2:
            self.vy = JUMPSPEED
            self.jumptimes += 1
            self.shiftState(JUMPUP)
        if jump == -1 and self.jumptimes == 0 and self.box.y > base:
            self.box.y -= 1
            self.shiftState(JUMPDOWN)

        collisionDetect(self)
        self.box.y += self.vy

        # x
        if direction == k_right:
            self.vx = PLAYERSPEED
            self.shiftState(MOVING)
            self.facing = 1
        elif direction == k_left:
            self.vx = -PLAYERSPEED
            self.shiftState(MOVING)
            self.facing = 0
        else:
            self.vx = 0
            self.shiftState(IDLE)
        if rush == 1:
            self.vx *= 15

        if self.box.x + self.vx + self.box.w > WIDTH:
            self.vx = 0
            self.box.x = WIDTH - self.box.w
            self.shiftState(IDLE)
        elif self.box.x + self.vx < 0:
            self.vx = 0
            self.box.x = 0
            self.shiftState(IDLE)
        self.box.x += self.vx

        # collision box update
        self.box.boxUpdate()
        
        # pic update
        t = time.time()
        if(t - self.lastTime[self.state[0]] > self.interval[self.state[0]]):
            self.picindex = (self.picindex + 1) % self.piclen[self.state[0]]
            self.lastTime[self.state[0]] = t

    def landing(self):
        if self.onground == 0:
            self.onground = 1
            self.jumptimes = 0
            self.vy = 0
            self.ay = 0
            self.shiftState(IDLE, pJUMP)

    def shiftState(self, state, piority = 10):
        if state[0] != self.state[0] and (state[1] <= self.state[1] or self.state[1] >= piority):
            self.picindex = 0
            self.state = state
    
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state[0]][self.picindex], (self.box.x, self.box.drawy))

    def takeDamage(self, damage):
        self.health -= damage
        
'''
    #sets harmbox
    def attackBegin(self):
        self.attacking = 1
        self.damage = 10
        self.harmbox = Rect(0, 0, self.w/2, self.h/2)
    def attack(self):
        if self.facing:
            self.harmbox.midleft = self.realbox.midleft
        else:
            self.harmbox.midright = self.realbox.midright
    def attackEnd(self):
        self.attacking = 1
'''

player_sources_right = [
    [pygame.image.load('./resources/graphicals/player_idle_1.png'),
    pygame.image.load('./resources/graphicals/player_idle_2.png'),
    pygame.image.load('./resources/graphicals/player_idle_3.png'),
    pygame.image.load('./resources/graphicals/player_idle_2.png'),],
    [pygame.image.load('./resources/graphicals/player_move_1.png'),
    pygame.image.load('./resources/graphicals/player_move_2.png'),
    pygame.image.load('./resources/graphicals/player_move_3.png'),
    pygame.image.load('./resources/graphicals/player_move_2.png'),],
    [pygame.image.load('./resources/graphicals/player_jump_up.png')],
    [pygame.image.load('./resources/graphicals/player_jump_down.png')],
    [pygame.image.load('./resources/graphicals/player_attack_1.png'),
    pygame.image.load('./resources/graphicals/player_attack_2.png')]]

player_sources_left = []
for i in range(0, len(player_sources_right)):
    player_sources_left.append([pygame.transform.flip(pic, True, False) for pic in player_sources_right[i]])
player_sources=[player_sources_left, player_sources_right]

player = Player(player_sources, initx, inity)
