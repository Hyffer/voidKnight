import pygame, sys, math, time
from pygame.locals import *
from starterlib import *

def terminate():
    pygame.quit()
    sys.exit()

def renderText(text):
    textImage = BASICFONT.render(text, True, WHITE)
    mainsurf.blit(textImage, (25, 25))
    pygame.display.update()

event_filter = [k_left, k_right]

list_enemy.append(PainBox(15, 200, 400))

s_welcome = 0
s_main = -1
s_pause = -2

def main():
    event_list = []
    rush = 0
    jump = 0
    attack = 0
    kRUSH = 0
    kJUMP = 0
    kFALL = 0
    switch = 1
    while switch == 1:
        # enemy loop
        for enemy in list_enemy:
            enemy.update()
            if player.attacking and enemy.hitbox.colliderect(player.harmbox):
                enemy.takeDamage()
            if enemy.attacking and player.hitbox.colliderect(enemy.harmbox):
                player.takeDamage(enemy.damage)

        #player event control loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in event_filter:
                    event_list.append(event.key)
                elif event.key == k_jump and kJUMP == 0:
                    if kFALL == 1:
                        jump = -1
                    else:
                        jump = 1
                    kJUMP = 1
                elif event.key == k_rush and kRUSH == 0:
                    rush = 1
                    kRUSH = 1
                elif event.key == k_down:
                    kFALL = 1
                # jump out
                elif event.key == k_pause:
                    switch = s_pause
        
            elif event.type == KEYUP:
                if event.key in event_filter:
                    event_list.remove(event.key)
                elif event.key == k_jump:
                    kJUMP = 0
                elif event.key == k_rush:
                    kRUSH = 0
                elif event.key == k_down:
                    kFALL = 0
        
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
        refreshScreen()
        fpsClock.tick(FPS)
    return switch

def welcome():
    renderText("WELCOME")
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    switch = s_main
            elif event.type == QUIT:
                terminate()
    return switch

def pause():
    renderText("PAUSE")
    switch = 1
    while switch == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == k_pause:
                    switch = s_main
            elif event.type == QUIT:
                terminate()
    return switch

pygame.init()

pygame.display.set_caption('voidKnight:')
BASICFONT = pygame.font.Font(None, 32)

switch = 0
while True:
    if switch == s_main:
        switch = main()
    elif switch == s_pause:
        switch = pause()
    elif switch == s_welcome:
        switch = welcome()
