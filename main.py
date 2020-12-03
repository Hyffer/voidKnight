import pygame, sys, math, time
from pygame.locals import *
from starterlib import *

stage_sources = [('./resources/graphicals/stage_bottom.png', (WINHALFWIDTH, 0)),
                 ('./resources/graphicals/stage_top.png', (WINHALFWIDTH, 64 )),
                 ('./resources/graphicals/stage_left.png', (WINHALFWIDTH - (128 + 16), 64 )),
                 ('./resources/graphicals/stage_right.png', (WINHALFWIDTH + 128 + 16, 64 ))]

<<<<<<< Updated upstream
player_sources = [
=======
list_still.append(Platform(0, 200, 200))

player_sources_right = [
>>>>>>> Stashed changes
    [pygame.image.load('./resources/graphicals/player_idle_1.png'),
    pygame.image.load('./resources/graphicals/player_idle_2.png'),
    pygame.image.load('./resources/graphicals/player_idle_3.png'),
    pygame.image.load('./resources/graphicals/player_idle_2.png'),],
    [pygame.image.load('./resources/graphicals/player_move_1.png'),
    pygame.image.load('./resources/graphicals/player_move_2.png'),
    pygame.image.load('./resources/graphicals/player_idle_3.png'),
    pygame.image.load('./resources/graphicals/player_move_2.png'),],]

for i, (x, y) in stage_sources:
    img = pygame.image.load(i)
    nomoveObj = noMove(img, (x, y), True)
    list_noMove.append(nomoveObj)

player = player(player_sources, [[pygame.transform.flip(i, True, False) for i in j] for j in player_sources], (100,64))

redraw()
origsurf = mainsurf.copy()
while True:
    playerEventHandle(player)

    mainsurf.blit(origsurf, (0,0))
    player.animate()
    player.draw()
    pygame.display.update()
    pygame.display.set_caption('void_knight: ')
    fpsClock.tick(FPS)
