"""
Cache simulation
"""

# tag0, tag1, LRU

CACHE_LINE_SIZE = 32
CACHE_LINE_NB = 256
cache = [(None, None, 0) for _ in range(CACHE_LINE_NB)]
hit = [0]
miss = [0]



def access2w(addr):
    l = (addr // CACHE_LINE_SIZE) % CACHE_LINE_NB
    tag = addr // CACHE_LINE_SIZE
    if cache[l][0] == tag or cache[l][1] == tag:
        # Hit
        cache[l] = (cache[l][0], cache[l][1], 0 if cache[l][0] == tag else 1)
        hit[0] += 1
        return True
    else:
        # Miss
        if cache[l][2] == 1:
            cache[l] = (tag, cache[l][1], 0)
        else:
            cache[l] = (cache[l][0], tag, 1)
        miss[0] += 1
        return False

X = 720
Y = 525


def run():
    for by in range(0, Y//8 + 1):
        for bx in range(0, X//8 + 1):
            for dy in range(-2, 2+1):
                for dx in range(-2, 2+1):
                    for j in range(8):
                        for i in range(8):
                            curx = bx * 8 + dx * 8 + i
                            cury = by * 8 + dy * 8 + j
                            addr = cury * X + curx
                            if not access2w(addr):
                                yield 0
                            # print(f'Access addr {addr} => {res}')
                            # curx = bx * 8 + i
                            # cury = by * 8 + j
                            # access2w(cury * X + curx)

    yield 1

import pygame

pygame.init()
screen = pygame.display.set_mode((X, Y), pygame.DOUBLEBUF)


prog = iter(run())

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # Core app
    for _ in range(10):
        next(prog)

    # Display
    screen.fill((255,255,255))
    # Draw cache
    for l in cache:
        for itag, tag in enumerate((l[0], l[1])):
            if tag is None:
                continue
            for addr in range(tag*CACHE_LINE_SIZE, tag*CACHE_LINE_SIZE+CACHE_LINE_SIZE):
                # if addr >= X * Y or addr < 0:
                #    continue
                x = addr % X
                y = addr // X
                screen.set_at((x, y), (255, 0, 0) if l[2] == itag else (255, 128, 128))
    # Draw Grid
    blockSize = 8 #Set the size of the grid block
    for x in range(0, X, blockSize):
        for y in range(0, Y, blockSize):
            rect = pygame.Rect(x, y, blockSize+1, blockSize+1)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    # Flip
    pygame.display.flip()
    print(f"{hit =} {miss =} {miss[0]/(hit[0]+miss[0]) =}")
    # input()


