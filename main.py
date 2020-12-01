import pygame, sys, math, time
from pygame.locals import *
from starterlib import *

stage_sources = [('./resources/graphicals/stage_bottom.png', (0, 0)),
                 ('./resources/graphicals/stage_top.png', (hWIDTH - 128, 64)),
                 ('./resources/graphicals/stage_left.png', (hWIDTH - 128 -32, 64)),
                 ('./resources/graphicals/stage_right.png', (hWIDTH + 128, 64))]
for i, (x, y) in stage_sources:
    img = pygame.image.load(i)
    obj = StillObj(img, x, y)
    list_still.append(obj)

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
    for i in list_still:
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
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                direction = 1
            if event.key == K_LEFT:
                direction = -1
        elif event.type == KEYUP:
            direction = 0
    
    player.update(direction)
    refreshScreen()
    fpsClock.tick(FPS)
