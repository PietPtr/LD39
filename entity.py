import pygame
import operator
import time

MOVETIME = 0.144

class Entity(object):
    def __init__(self, pos, rules):
        self.pos = pos
        self.rules = rules
        self.index = 0
        self.last_move_time = time.time()
        self.last_move = [0, 0]

    def move(self):
        direction = self.rules[self.index % len(self.rules)]
        self.pos[0] += direction[0]
        self.pos[1] += direction[1]
        self.index += 1
        self.last_move_time = time.time()
        self.last_move = direction[:]

    def draw(self, screen, width, height):
        # entrect = pygame.Rect(self.pos[0] * width / 16, \
        #     self.pos[1] * height / 9, width / 16, height / 9)
        #
        # pygame.draw.rect(screen, (100, 100, 100), entrect)

        time_since_move = time.time() - self.last_move_time
        if time_since_move > MOVETIME:
            time_since_move = MOVETIME

        x = (self.pos[0] - self.last_move[0]) * width / 16 + (width / 16) \
                * time_since_move * 1 / MOVETIME * self.last_move[0]
        y = (self.pos[1] - self.last_move[1]) * height / 9 + (height / 9) \
                * time_since_move * 1 / MOVETIME * self.last_move[1]

        entrect = pygame.Rect(x, y, width / 16, height / 9)

        pygame.draw.rect(screen, (100, 100, 100), entrect)
