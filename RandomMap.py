import random

from basis import HEIGHT, WIDTH

sources = [('./resources/graphicals/platform_M.png', 200),
           ('./resources/graphicals/platform_L.png', 400),
           ('./resources/graphicals/platform_XL.png', 750)]
added_sources = []

def randomMap():
    h = random.randint(245, 300)
    while h + 130 < HEIGHT:
        pic, wth = random.choice(sources)
        x = random.randint(0, WIDTH - wth)
        added_sources.append((pic, (x, h)))
        h += random.randint(80, 240)
