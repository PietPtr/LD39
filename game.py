import sys, pygame, math, time
from pygame.locals import *
from player import Player
from entity import Entity

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
pygame.font.init()

size = width, height = 1280, 720
black = 41, 43, 44
grey = 193, 193, 193
white = 247, 247, 249

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Float')

font = pygame.font.SysFont('Monospace', 30)

step_wav = pygame.mixer.Sound('./sound/step.wav')
next_wav = pygame.mixer.Sound('./sound/next.wav')
thud_wav = pygame.mixer.Sound('./sound/thud.wav')

entities = []
entity_rules = [[(0, 1), (0, -1)],
                [(0, -1), (0, 1)],
                [(0, 1), (1, 0), (0, -1), (-1, 0)],
                [(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 1)],
                [(0, 0),(0, 0),(0, 0),(0, 1),(0, 0),(0, -1)]]
move_entities = True

def load_level(n):
    lvlstr = open('./levels/' + str(n), 'r').read().split('\n')[1:]
    lvlstr = '\n'.join(lvlstr)

    level = [[]]

    row = 0
    for tile in lvlstr:
        if tile != '\n':
            if int(tile) > 2:
                level[row].append(0)
            else:
                level[row].append(int(tile))
        else:
            row += 1
            level.append([])

    return level

def load_player(n):
    plr = open('./levels/' + str(n), 'r').read().split('\n')[0].split(',')

    return Player([int(plr[0]), int(plr[1])], int(plr[2]))

def load_entities(n):
    entstr = open('./levels/' + str(n), 'r').read().split('\n')[1:]

    entities = []

    y = 0
    for row in entstr:
        x = 0
        for tile in row:
            if int(tile) > 2:
                entities.append(Entity([x, y], entity_rules[int(tile) - 3]))
            x += 1
        y += 1

    return entities


def draw_tile(tile, x, y):
    if tile == 0:
        pygame.draw.rect(screen, black, pygame.Rect(x * width/16, y * height/9,\
            width/16, height/9))
        pygame.draw.rect(screen, (21, 23, 24), pygame.Rect(x * width/16, y * height/9,\
            width/16, height/9), 1)
    if tile == 1:
        pygame.draw.rect(screen, grey, pygame.Rect(x * width/16, y * height/9,\
            width/16, height/9))
    if tile == 2:
        pygame.draw.rect(screen, white, pygame.Rect(x * width/16, y * height/9,\
            width/16, height/9))

def can_walk(pos):
    if get_tile(pos) not in [0, 2]:
        return False

    for entity in entities:
        if pos == entity.pos:
            return False

    return True

def get_tile(pos):
    return level[pos[1]][pos[0]]

def move_player(direction):
    global level
    global player
    global entities
    global num_lvl

    #print(round(time.time() * 1000))

    if player.power == -1:
        reset()
        return

    for entity in entities:
        entity.move()

    player.move(direction)

    if not player.moved:
        thud_wav.play()

num_lvl = 1
level = load_level(num_lvl)
player = load_player(num_lvl)
player.move([0, 0])                             # 'Excellent code' - Mrtijn 2017
entities = load_entities(num_lvl)

old_player_pos = player.get_pos()

starttime = time.time()
endtime = 0


def reset():
    global level
    global player
    global entities
    global num_lvl

    level = load_level(num_lvl)
    player = load_player(num_lvl)
    entities = load_entities(num_lvl)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            size = event.size
            width = event.w
            height = event.h
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player([0, -1])
            if event.key == pygame.K_DOWN:
                move_player([0, 1])
            if event.key == pygame.K_LEFT:
                move_player([-1, 0])
            if event.key == pygame.K_RIGHT:
                move_player([1, 0])

    screen.fill(black)

    # updating

    if get_tile(player.get_pos()) is 2:
        next_wav.play()
        if num_lvl == 99:
            num_lvl = 1
            reset()
            starttime = time.time()
            continue

        print('power: ', player.power)
        num_lvl += 1
        try:
            reset()
        except IOError:
            num_lvl = 99
            endtime = time.time()
            reset()

    for entity in entities:
        if entity.pos == player.grid_pos:
            reset()

    # drawing

    y = 0
    for row in level:
        x = 0
        for tile in row:
            draw_tile(tile, x, y)
            x += 1
        y += 1

    player.draw(screen, width, height)

    for entity in entities:
        entity.draw(screen, width, height)

    if num_lvl == 99:
        timetext = font.render('You completed the game in ' + \
            str(round(endtime - starttime, 2)) + ' seconds!', False, white)

        screen.blit(timetext, (width / 2 - timetext.get_width() / 2, \
            height - font.get_height() - 10))

    pygame.display.flip()
