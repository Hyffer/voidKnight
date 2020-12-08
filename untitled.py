import pygame, time
from pygame.locals import *
from basis import *

class Player(MovableObj):
    def __init__(self, pic):
        MovableObj.__init__(self, hWIDTH, 128)
        self.pic = pic
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        self.interval = [IDLEINTERVAL, MOVEINTERVAL, NOINTERVAL, NOINTERVAL, ATTACKINTERVAL]
        self.lastTime = [0, 0, 0, 0, 0]
        self.w, self.h = pic[0][0][0].get_size()
        self.hp = 100
        #player attack box
        self.harmbox = None
        #actual player image box
        self.realbox = self.pic[0][0][0].get_rect()
        #player hitbox
        self.hitbox = self.realbox.inflate(-(self.w - HITBOXW), 0)
    def update(self, direction, rush, jump, attack):
        # collision box update
        self.rect_l = self.x
        self.rect_r = self.x + self.w
        
        # moving state update
        # y
        if jump == 1 and self.leaveground < 2:
            self.vy = JUMPSPEED
            self.leaveground += 1
            self.shiftState(JUMPUP)
        if jump == -1 and self.leaveground == 0 and self.y > base:
            self.y -= 1
            self.shiftState(JUMPDOWN)

        collideDetect(self)
        self.y += self.vy

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

        if self.x + self.vx + self.w > WIDTH:
            self.vx = 0
            self.x = WIDTH - self.w
            self.shiftState(IDLE)
        elif self.x + self.vx < 0:
            self.vx = 0
            self.x = 0
            self.shiftState(IDLE)
        self.x += self.vx

        #box update
        self.realbox.midbottom = self.pygamecoord()
        self.hitbox.midbottom = self.pygamecoord()
        # pic update
        t = time.time()
        if(t - self.lastTime[self.state] > self.interval[self.state]):
            self.picindex = (self.picindex + 1) % self.piclen[self.state]
            self.lastTime[self.state] = t

    def landing(self):
        if self.state in player_state_ctn:
            self.state = IDLE
            self.picindex = 0
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
    def takeDamage(self, damage):
        self.hp -= damage
        print('ow: ', self.hp)
    def shiftState(self, state):
        if self.state != state and not self.state in player_state_ctn:
            self.picindex = 0
            self.state = state
    def draw(self):
        mainsurf.blit(self.pic[self.facing][self.state][self.picindex], (self.x, HEIGHT - self.y - self.h))

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
