import pygame
from pygame.locals import *
from basis import *

class Platform(StillObj):
    def __init__(self, img, x, y):
        StillObj.__init__(self, img, x, y)
        w, h = img.get_size()
        self.rect_t = y + h
        self.rect_l = x
        self.rect_r = x + w

platform_sources = [('./resources/graphicals/stage_bottom.png', (0, 0)),
                    ('./resources/graphicals/stage_top.png', (hWIDTH - 128, 64)),
                    ('./resources/graphicals/stage_left.png', (hWIDTH - 128 -32, 64)),
                    ('./resources/graphicals/stage_right.png', (hWIDTH + 128, 64)),
                    ('./resources/graphicals/platform_M.png', (hWIDTH, 500)),
                    ('./resources/graphicals/platform_L.png', (25, 300))]
for i, (x, y) in platform_sources:
    img = pygame.image.load(i)
    obj = Platform(img, x, y)
    list_platform.append(obj)
