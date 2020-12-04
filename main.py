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

pygame.init()
pygame.display.set_caption('voidKnight:')
refreshScreen()
direction = 0
jump = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_d:
                direction = 1
            if event.key == K_a:
                direction = -1
            if event.key == K_SPACE:
                jump = 1
        elif event.type == KEYUP:
            if event.key == K_d or event.key == K_a:
                direction = 0
            if event.key == K_SPACE:
                jump = 0

    player.update(direction, jump)
    refreshScreen()
    fpsClock.tick(FPS)
