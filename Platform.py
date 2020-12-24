import pygame
from pygame.locals import *

from basis import *
from RandomMap import *

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

platform_sources = [('./resources/graphicals/stage_bottom.png', (0, 0))]

randomMap()
platform_sources.extend(added_sources)

index = 0
for i, (x, y) in platform_sources:
    img = pygame.image.load(i)
    obj = Platform(index, img, x, y)
    index += 1
    list_platform.append(obj)

# --- track ---
def deltaxMAX(deltah):
    return (UPTIME + (2*(deltah-JUMPHEIGHT)/G)**0.5) * ENEMYSPEED

# create self.reach
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
    
# self.route list init
for platform in list_platform:
    for obj in list_platform:
        platform.route.append(-1)

# create self.route
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

for platform in list_platform:
    for obj in list_platform:
        if platform == obj:
            continue
        route = []
        routing(platform.index, obj.index)

# shorten route
for platform in list_platform:
    for i in range(0, len(list_platform)):
        if i == platform.index:
            continue
        p = list_platform[platform.route[i]]
        while p.route[i] >= 0:
            if p.route[i] in platform.reach:
                platform.route[i] = p.route[i]
            p = list_platform[p.route[i]]

if __name__ == '__main__':
    for platform in list_platform:
        print(platform.reach)
        print(platform.route)
        print("")
