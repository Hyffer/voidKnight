import pygame, sys, math, time
from pygame.locals import *
from starterlib import *

def terminate():
    pygame.quit()
    sys.exit()

event_filter = [k_left, k_right]
event_list = []

pygame.init()
pygame.display.set_caption('Void Knight')
refreshScreen()
rush = 0
jump = 0
attacking = 0
kRUSH = 0
kJUMP = 0
kFALL = 0

list_enemy.append(PainBox(15, 200, 400))

while True:
    #enemy loop
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
            elif event.key == k_attack and attacking == 0:
                attacking = 1
        
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
    player.update(direction, rush, jump, attacking)
    jump = 0
    rush = 0


    refreshScreen()
    fpsClock.tick(FPS)
