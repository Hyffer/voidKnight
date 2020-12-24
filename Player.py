import pygame, time
from pygame.locals import *
from basis import *

initx       = 200
inity       = base


sounds_footsteps = [pygame.mixer.Sound('./resources/audiables/footstep_concrete_000.ogg'),
                  pygame.mixer.Sound('./resources/audiables/footstep_concrete_001.ogg'),
                  pygame.mixer.Sound('./resources/audiables/footstep_concrete_002.ogg'),
                  pygame.mixer.Sound('./resources/audiables/footstep_concrete_003.ogg'),
                  pygame.mixer.Sound('./resources/audiables/footstep_concrete_004.ogg')]

class Player(MovableObj):
    def __init__(self, pic):
        # picture init
        self.pic = pic
        self.piclen = [len(pic[0][i]) for i in range(len(pic[0]))]
        self.picindex = 0
        # collision box init
        w, h = pic[0][0][0].get_size()
        self.box = Box(w, h)
        self.damagebox = Box(wDAMAGEBOX, self.box.h)
        self.damage = 20
        self.mass = PLAYERMASS
        self.knockback = 20
        self.knockbackvx = 0
        self.lastTime = [0, 0, 0, 0, 0]
        self.lastFootstep = 0
        self.footstepInterval = 0.3
        self.lastTimeInvincible = 0
        self.interval = [IDLEINTERVAL, MOVEINTERVAL, NOINTERVAL, NOINTERVAL, ATTACKINTERVAL]
        self.build()
    def build(self):
        # health, movable states and position
        self.invincible = 0
        self.health = PLAYERHEALTH
        MovableObj.__init__(self)
        self.box.setPosition(initx, inity)
        
    def update(self, direction, rush, jump, attack):
        # moving state update
        # y
        if jump == 1:
            self.jump()
        if jump == -1:
            self.jumpdown()

        if attack == 1:
            self.attacking = 1
            self.shiftState(ATTACK)
            self.damagebox.setPosition(self.box.centerx + (self.facing*2-1)*self.damagebox.w/2, self.box.y)
            self.lastTime[ATTACK[0]] = time.time()

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
            self.vx *= PLAYERRUSHBONUS

        if self.box.x + self.vx + self.box.w > WIDTH:
            self.vx = 0
            self.box.centerx = WIDTH - self.box.w/2
            self.shiftState(IDLE)
        elif self.box.x + self.vx < 0:
            self.vx = 0
            self.box.centerx = 0 + self.box.w/2
            self.shiftState(IDLE)

        if self.knockbackvx != 0:
            self.vx += self.knockbackvx
            self.knockbackvx = chip(self.knockbackvx, self.mass)

        # collision box update
        self.box.moving(self.vx, self.vy)
        if self.attacking:
            self.damagebox.moving(self.vx, self.vy)
        
        # pic update
        t = time.time()
        if(t - self.lastTime[self.state[0]] > self.interval[self.state[0]]):
            self.picindex = (self.picindex + 1) % self.piclen[self.state[0]]
            self.lastTime[self.state[0]] = t
        
        if self.state == MOVING and self.onground == 1 and t - self.lastFootstep> self.footstepInterval:
            random.choice(sounds_footsteps).play()
            self.lastFootstep = t
        if self.state == ATTACK and self.picindex == self.piclen[ATTACK[0]] -1:
            self.shiftState(IDLE, pATTACK)
            self.attacking = 0
        if self.invincible and t - self.lastTimeInvincible > INVINCIBILITYTIME:
            self.invincible = 0
    
    def draw(self):
        #self.box.show(GREEN)
        if self.invincible == 0 or int(((time.time() - self.lastTimeInvincible)/INVINCIBILITYINTERVAL))%2:
            img = self.pic[self.facing][self.state[0]][self.picindex]
            w, h = img.get_size()
            mainsurf.blit(img, (self.box.centerx - w/2, self.box.drawy))
        self.box.show(GREEN)
        if self.attacking:
            self.damagebox.show()

    def takeDamage(self, damage, towards, knockback):
        if not self.invincible:
            self.health -= damage
            self.invincible = 1
            self.lastTimeInvincible = time.time()
            self.knockbackvx = (towards * 2 - 1)* knockback
            self.vy = 10

    def causeDamage(self, enemybox):
        if self.damagebox.isCollideWith(enemybox):
            return self.damage
        return 0

player_sources_right = [
    [pygame.image.load('./resources/graphicals/player/idle_001.png'),
    pygame.image.load('./resources/graphicals/player/idle_002.png'),
    pygame.image.load('./resources/graphicals/player/idle_003.png'),
    pygame.image.load('./resources/graphicals/player/idle_002.png'),],
    [pygame.image.load('./resources/graphicals/player/run_000.png'),
    pygame.image.load('./resources/graphicals/player/run_001.png'),
    pygame.image.load('./resources/graphicals/player/run_002.png'),
    pygame.image.load('./resources/graphicals/player/run_003.png'),
    pygame.image.load('./resources/graphicals/player/run_004.png'),
    pygame.image.load('./resources/graphicals/player/run_005.png'),],
    [pygame.image.load('./resources/graphicals/player/jump_003.png')],
    [pygame.image.load('./resources/graphicals/player/fall_000.png'),
     pygame.image.load('./resources/graphicals/player/fall_001.png'),],
    [pygame.image.load('./resources/graphicals/player/attack_002.png'),
    pygame.image.load('./resources/graphicals/player/attack_003.png'),
    pygame.image.load('./resources/graphicals/player/attack_004.png'),
    pygame.image.load('./resources/graphicals/player/attack_005.png'),
     pygame.image.load('./resources/graphicals/player/attack_000.png'),]]

for i in range(len(player_sources_right)):
    for j in range(len(player_sources_right[i])):
        img = player_sources_right[i][j]
        w,h  = img.get_size()
        player_sources_right[i][j] = pygame.transform.scale(img, (int(w * 1.35), int(h * 1.35)))
player_sources_left = []
for i in range(0, len(player_sources_right)):
    player_sources_left.append([pygame.transform.flip(pic, True, False) for pic in player_sources_right[i]])
player_sources=[player_sources_left, player_sources_right]

player = Player(player_sources)
list_player.append(player)
