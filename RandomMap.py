import random

from basis import HEIGHT, WIDTH
from Platform import *

# --- track ---
def deltaxMAX(deltah):
    return (UPTIME + (2*(deltah-JUMPHEIGHT)/G)**0.5) * ENEMYSPEED

def routing(begin, end, route):
    route.append(begin)
    if end in list_platform[begin].reach:
        list_platform[begin].route[end] = end
        return 1
    for nextbegin in list_platform[begin].reach:
        if nextbegin in route:
            continue
        if routing(nextbegin, end, route):
            list_platform[begin].route[end] = nextbegin
            return 1

def mapping():
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
    for platform in list_platform:
        for obj in list_platform:
            if platform == obj:
                continue
            route = []
            routing(platform.index, obj.index, route)

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

sources = [('./resources/graphicals/platform_M.png', 200),
           ('./resources/graphicals/platform_L.png', 400),
           ('./resources/graphicals/platform_XL.png', 750)]

def randomMap():
    platform_sources = [('./resources/graphicals/stage_bottom.png', (0, 0))]
    h = random.randint(245, 300)
    while h + 130 < HEIGHT:
        pic, wth = random.choice(sources)
        x = random.randint(0, WIDTH - wth)
        platform_sources.append((pic, (x, h)))
        h += random.randint(80, 240)

    index = 0
    for i, (x, y) in platform_sources:
        img = pygame.image.load(i)
        obj = Platform(index, img, x, y)
        index += 1
        list_platform.append(obj)

    mapping()
