import pygame, sys, math, time
from pygame.locals import *
from starterlib import *

player_sources_right = [
    [pygame.image.load('./resources/graphicals/player_idle_1.png'),
    pygame.image.load('./resources/graphicals/player_idle_2.png'),
    pygame.image.load('./resources/graphicals/player_idle_3.png'),
    pygame.image.load('./resources/graphicals/player_idle_2.png'),],
    [pygame.image.load('./resources/graphicals/player_move_1.png'),
    pygame.image.load('./resources/graphicals/player_move_2.png'),
    pygame.image.load('./resources/graphicals/player_move_3.png'),
    pygame.image.load('./resources/graphicals/player_move_2.png'),],]

player_sources_left = []
for i in range(0, len(player_sources_right)):
    player_sources_left.append([pygame.transform.flip(pic, True, False) for pic in player_sources_right[i]])
player_sources=[player_sources_left, player_sources_right]

player = Player(player_sources)

def refreshScreen():
    mainsurf.fill((0, 0, 0))
    for i in list_platform:
        i.draw()
    player.draw()
    pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()

event_filter = [K_a, K_d]
event_list = []

pygame.init()
pygame.display.set_caption('voidKnight:')
refreshScreen()
direction = 0
jump = 0
kw = 0
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key in event_filter:
            event_list.append(event.key)
        elif event.type == KEYDOWN:
            if event.key == K_w and kw == 0:
                jump = 1
                kw = 1
            if event.key == K_s:
                jump = -1
        elif event.type == KEYUP and event.key in event_filter:
            event_list.remove(event.key)
        elif event.type == KEYUP:
            if event.key == K_w:
                kw = 0
        elif event.type == QUIT:
            terminate()

    event_len = len(event_list)
    if event_len != 0:
        direction = event_list[event_len - 1]
    else:
        direction = 0
    player.update(direction, jump)
    jump = 0
    
    refreshScreen()
    fpsClock.tick(FPS)
