import pygame
from pygame.locals import *
from basis import *

class Platform(StillObj):
    def __init__(self, index, img, x, y):
        StillObj.__init__(self, img, x, y)
        w, h = img.get_size()
        self.rect_t = y + h
        self.rect_l = x
        self.rect_r = x + w
        self.index = index
        self.reach = []
        self.route = []

platform_sources = [('./resources/graphicals/stage_bottom.png', (0, 0)),
                    ('./resources/graphicals/platform_M.png', (hWIDTH, 500)),
                    ('./resources/graphicals/platform_L.png', (25, 300)),
                    ('./resources/graphicals/platform_M.png', (0, 650)),]
index = 0
for i, (x, y) in platform_sources:
    img = pygame.image.load(i)
    obj = Platform(index, img, x, y)
    index += 1
    list_platform.append(obj)

def deltaxMAX(deltah):
    return (UPTIME + ((deltah-JUMPHEIGHT)/G)**0.5) * ENEMYSPEED

# create map
for platform in list_platform:
    for obj in list_platform:
        deltah = obj.rect_t - platform.rect_t
        if obj == platform or deltah - JUMPHEIGHT > -10:
            continue
        elif obj.rect_l <= platform.rect_r and obj.rect_r >= platform.rect_l:
            platform.reach.append(obj.index)
        elif obj.rect_l > platform.rect_r and obj.rect_l - platform.rect_r <= deltaxMAX(deltah):
            platform.reach.append(obj.index)
        elif obj.rect_r < platform.rect_l and platform.rect_l - obj.rect_r <= deltaxMAX(deltah):
            platform.reach.append(obj.index)

route = []
def routing(begin, end):
    route.append(begin)
    if end in list_platform[begin].reach:
        list_platform[begin].route[end] = end
        return 1
    for nextbegain in list_platform[begin].reach:
        if nextbegain in route:
            continue
        if routing(nextbegain, end):
            list_platform[begin].route[end] = nextbegain
            return 1
    
# route init
for platform in list_platform:
    for obj in list_platform:
        platform.route.append(-1)

# compute route
for platform in list_platform:
    for obj in list_platform:
        if platform == obj:
            continue
        route = []
        routing(platform.index, obj.index)
        

if __name__ == '__main__':
    for platform in list_platform:
        print(platform.reach)
        print(platform.route)
        print("")
