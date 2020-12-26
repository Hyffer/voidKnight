import pygame, sys, math, time

pygame.init()
pygame.mixer.init()

from pygame.locals import *
from basis import *
from RandomMap import *
from Player import *
from Enemy import *
from Spawner import *

rtC     = 0
rtTL    = 1
rtTR    = 2

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
                if event.key in event_filter:
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
                player.takeDamage(enemy.damage)
            if player.health <= 0:
                switch = s_dead
            if attack and enemy.box.isCollideWith(player.damagebox):
                enemy.takeDamage(player.facing, player.damage)

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
                    switch = s_main
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if startrect.collidepoint(mousex, mousey):
                    switch = s_main
                if quitrect.collidepoint(mousex, mousey):
                    terminate()
            elif event.type == QUIT:
                terminate()
        fpsClock.tick(FPS)
    return switch

def pause():
    # mist
    mainsurf.blit(mistrect, (0, 0))
    renderText("PAUSE")
    pygame.display.update()
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
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
        switch = welcome()
