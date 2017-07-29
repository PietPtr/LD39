import pygame
import operator

class Entity(object):
    def __init__(self, pos, rules):
        self.pos = pos
        self.rules = rules
        self.index = 0

    def move(self):
        direction = self.rules[self.index % len(self.rules)]
        self.pos[0] += direction[0]
        self.pos[1] += direction[1]
        self.index += 1

    def draw(self, screen, width, height):
        entrect = pygame.Rect(self.pos[0] * width / 16, \
            self.pos[1] * height / 9, width / 16, height / 9)

        pygame.draw.rect(screen, (100, 100, 100), entrect)
