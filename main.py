import pygame, sys, math, time
from pygame.locals import *
from basis import *
from Platform import *
from Player import *
from Enemy import *
from Spawner import *

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

    pygame.display.update()

def drawHealth():
    percentage = player.health / PLAYERHEALTH
    if percentage > 0.8 or int((time.time()*10))%2:
        healthcolor = WHITE
    else :
        healthcolor = RED
    pygame.draw.rect(mainsurf, healthcolor, (50,50,200*percentage,20))
    pygame.display.update()

def renderText(text, base = 'C', position = (25, 50), font = None, size = 32):
    font = pygame.font.Font(font, size)
    textImage = font.render(text, True, WHITE)
    textRect = textImage.get_rect()
    if base == 'C':
        textRect.center = position
    elif base == 'BL':
        textRect.bottomleft = position
    mainsurf.blit(textImage, textRect)
    pygame.display.update()
    return textRect

event_filter = [k_left, k_right]

s_welcome = 0
s_main = -1
s_pause = -2
s_dead = -3

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
                    kFALL = 1
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
                    kFALL = 0
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
            if player.box.isCollideWith(enemy.damagebox) and enemy.attacking:
                player.takeDamage(enemy.damage)
            if player.health <= 0:
                switch = s_dead
            if attack and enemy.box.isCollideWith(player.damagebox):
                enemy.takeDamage(player.damage)

        # end player damage
        attack = 0

        gate.update()
        # refresh screen
        refreshScreen()
        renderText("HP:" + str(player.health), base = 'BL')
        drawHealth()
        fpsClock.tick(FPS)
        
    return switch

def welcome():
    mainsurf.fill((0, 0, 0))
    renderText("WELCOME", base = 'BL')
    startrect = renderText("Start Game", position=(hWIDTH, HEIGHT /2), size = 100)
    quitrect = renderText("Quit", position=(hWIDTH, HEIGHT * 0.75), size = 40)
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
        pygame.display.update()
        fpsClock.tick(FPS)
    return switch

def pause():
    renderText("PAUSE", base = 'BL', position = (WIDTH - 100, 25))
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    switch = s_main
            elif event.type == QUIT:
                terminate()
    return switch

def dead():
    mainsurf.fill((0, 0, 0))
    renderText("DEAD", base = 'BL')
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    # rebuild
                    for e in list_enemy:
                        e.build()
                    player.build()
                    switch = s_main
            elif event.type == QUIT:
                terminate()
    return switch

pygame.init()

pygame.display.set_caption('voidKnight:')
DEFAULTFONT = None

switch = 0
while True:
    if switch == s_main:
        switch = main()
    elif switch == s_pause:
        switch = pause()
    elif switch == s_dead:
        switch = dead()
    elif switch == s_welcome:
        switch = welcome()
