import pygame, time
from pygame.locals import *
from basis import *

initx       = hWIDTH
inity       = 64

class Player(MovableObj):
    def __init__(self, pic):
        # picture init
        self.pic = pic
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        # collision box init
        w, h = pic[0][0][0].get_size()
        self.box = Box(w, h)
        self.lastTime = [0, 0, 0, 0, 0]
        self.interval = [IDLEINTERVAL, MOVEINTERVAL, NOINTERVAL, NOINTERVAL, ATTACKINTERVAL]
        self.build()
    def build(self):
        # health, movable states and position
        self.health = 500
        MovableObj.__init__(self)
        self.box.setPosition(initx, inity)
        
    def update(self, direction, rush, jump, attack):
        # moving state update
        # y
        if jump == 1:
            self.jump()
        if jump == -1:
            self.jumpdown()

        fdreturn = self.fallingDetection()
        if fdreturn != -1:
            self.standOn = fdreturn

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
            self.box.centerx = WIDTH - self.box.w/2
            self.shiftState(IDLE)
        elif self.box.x + self.vx < 0:
            self.vx = 0
            self.box.centerx = 0 + self.box.w/2
            self.shiftState(IDLE)

        # collision box update
        self.box.moving(self.vx, self.vy)
        
        # pic update
        t = time.time()
        if(t - self.lastTime[self.state[0]] > self.interval[self.state[0]]):
            self.picindex = (self.picindex + 1) % self.piclen[self.state[0]]
            self.lastTime[self.state[0]] = t
    
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

player = Player(player_sources)
list_player.append(player)
