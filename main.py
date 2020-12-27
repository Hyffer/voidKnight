import pygame, sys, math, time

pygame.init()
pygame.mixer.init()
music = pygame.mixer.music

from pygame.locals import *
from basis import *
from RandomMap import *
from Player import *
from Enemy import *
from Spawner import *

rtC     = 0
rtTL    = 1
rtTR    = 2

MAINMUSIC = './resources/audiables/bg_music/bonebottom.mp3'
BATTLEMUSIC = './resources/audiables/bg_music/eternity.mp3'
NORMALVOLUME= 0.7
PAUSEVOLUME = 0.1

def terminate():
    pygame.quit()
    sys.exit()

def refreshScreen():
    mainsurf.fill((0, 0, 0))
    for i in list_platform:
        i.draw()
    gate.draw()
    for i in list_enemy:
        i.draw()
    player.draw()

def drawHealth():
    percentage = player.health / PLAYERHEALTH
    if percentage > 0.2 or int((time.time()*10))%2:
        healthcolor = WHITE
    else :
        healthcolor = RED
    pygame.draw.rect(mainsurf, healthcolor, (WIDTH-25-200*percentage, 5 , 200*percentage, 20))

def renderText(text, base = rtTL, position = (25, 27), font = FONT, size = 32):
    font = pygame.font.Font(font, size)
    textImage = font.render(text, True, WHITE)
    textRect = textImage.get_rect()
    if base == rtC:
        textRect.center = position
    elif base == rtTL:
        textRect.topleft = position
    elif base == rtTR:
        textRect.topright = position
    mainsurf.blit(textImage, textRect)
    return textRect

event_filter = [k_left, k_right]

s_welcome   = 0
s_main      = -1
s_pause     = -2
s_win       = -3
s_dead      = -4

def restart():
    resetList()
    randomMap()
    player.build()
    score[0] = 0

def main():
    event_list = []
    jump = 0
    rush = 0
    attack = 0
    kJUMP = 0
    kDOWN = 0
    kRUSH = 0
    kATTACK = 0
    switch = 1
    while switch == 1:
        # player event loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in event_filter:
                    event_list.append(event.key)
                elif event.key == k_jump and kJUMP == 0:
                    if kDOWN == 1:
                        jump = -1
                    else:
                        jump = 1
                    kJUMP = 1
                elif event.key == k_down:
                    kDOWN = 1
                elif event.key == k_rush and kRUSH == 0:
                    rush = 1
                    kRUSH = 1
                elif event.key == k_attack and kATTACK == 0 and player.state != ATTACK:
                    attack = 1
                    kATTACK = 1

                # jump out
                elif event.key == k_pause:
                    switch = s_pause
        
            elif event.type == KEYUP:
                if event.key in event_filter and event.key in event_list:
                    event_list.remove(event.key)
                elif event.key == k_jump:
                    kJUMP = 0
                elif event.key == k_down:
                    kDOWN = 0
                elif event.key == k_rush:
                    kRUSH = 0
                elif event.key == k_attack:
                    kATTACK = 0
        
            elif event.type == QUIT:
                terminate()

        event_len = len(event_list)
        if event_len != 0:
            direction = event_list[event_len - 1]
        else:
            direction = 0
        player.update(direction, rush, jump, attack)
        jump = 0
        rush = 0

        # enemy loop
        for enemy in list_enemy:
            enemy.update()
            if enemy.box.isCollideWith(player.box) and enemy.attacking:
                player.takeDamage(enemy.damage, enemy.facing, enemy.knockback + random.randint(-5, 5))
            if player.health <= 0:
                switch = s_dead
            if player.attacking and enemy.box.isCollideWith(player.damagebox):
                player.health += PLAYERREGEN * enemy.takeDamage(player.facing, player.damage, player.knockback + random.randint(-5, 5))
        player.health = clip(player.health, PLAYERHEALTH)
        # end player attack
        attack = 0

        gate.update()

        #if len(list_enemy) == 0:
        #    switch = s_win
        
        # refresh screen
        refreshScreen()
        renderText("HP:" + str(player.health), base = rtTR, position = (WIDTH-25, 27))
        drawHealth()
        renderText('SLAIN:' + str(score[0]), base = rtTL, position = (15, 50))
        pygame.display.update()

        # repeat music


        fpsClock.tick(FPS)
        
    return switch

def welcome():
    mainsurf.fill((0, 0, 0))
    renderText("VOID KNIGHT", base = rtC, font=FONTTITLE, position = (hWIDTH, 100), size = 100)
    startrect = renderText("Start Game", base = rtC, position=(hWIDTH, HEIGHT /2), size = 40)
    quitrect = renderText("Quit", base = rtC, position=(hWIDTH, HEIGHT * 0.75), size = 40)
    pygame.display.update()
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    music.load(BATTLEMUSIC)
                    music.set_volume(0.7)
                    music.play(-1)
                    switch = s_main
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                sounds_click.play()
                if startrect.collidepoint(mousex, mousey):
                    music.load(BATTLEMUSIC)
                    music.set_volume(NORMALVOLUME)
                    music.play(-1)
                    switch = s_main
                if quitrect.collidepoint(mousex, mousey):
                    terminate()
            elif event.type == QUIT:
                terminate()
        fpsClock.tick(FPS)
    return switch

def pause():
    # mist
    sounds_click.play()
    mainsurf.blit(mistrect, (0, 0))
    pauserect = renderText("PAUSED",base = rtC , position=(hWIDTH, HEIGHT/2), size = 80)
    mainsurf.blit(pause_icon, (pauserect.left - 100, pauserect.centery-50))

    music.set_volume(PAUSEVOLUME)
    pygame.display.update()
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    sounds_click.play()
                    music.set_volume(NORMALVOLUME)
                    switch = s_main
            elif event.type == QUIT:
                terminate()
    return switch

def win():
    mainsurf.fill((0, 0, 0))
    renderText("WIN")
    pygame.display.update()
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    restart()
                    switch = s_main
            elif event.type == QUIT:
                terminate()
    return switch

def dead():
    mainsurf.fill((0, 0, 0))
    renderText("DEAD")
    pygame.display.update()
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    restart()
                    switch = s_main
            elif event.type == QUIT:
                terminate()
    return switch

# load minor resources
pause_icon = pygame.image.load('./resources/graphicals/icon/pause.png')

pygame.display.set_caption('voidKnight')
pygame.display.set_icon(pygame.image.load('./resources/graphicals/icon/gameicon.png'))
DEFAULTFONT = None

player = Player()
list_player.append(player)
randomMap()

switch = 0
while True:
    if switch == s_main:
        switch = main()
    elif switch == s_pause:
        switch = pause()
    elif switch == s_dead:
        switch = dead()
    elif switch == s_win:
        switch = win()
    elif switch == s_welcome:
        music.load(MAINMUSIC)
        music.play(-1)
        music.set_volume(1.0)
        switch = welcome()
