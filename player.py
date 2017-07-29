import pygame

class Player(object):
    def __init__(self, grid_position, power):
        self.grid_pos = grid_position
        self.init_pos = grid_position
        self.power = power
        self.max_pow = power
        self.moved = False

    def can_move(self, direction):
        old_pos = self.grid_pos[:]
        new_pos = self.grid_pos[:]
        new_pos[0] += direction[0]
        new_pos[1] += direction[1]

        if new_pos[0] < 0 or new_pos[0] >= 16:
            new_pos = old_pos
        if new_pos[1] < 0 or new_pos[1] >= 9:
            new_pos = old_pos

        from game import can_walk
        if not can_walk(new_pos):
            new_pos = old_pos

        if new_pos != old_pos and self.power > 0:
            return new_pos
        else:
            return False

    def move(self, direction):
        new_pos = self.can_move(direction) # new_pos is either False, or a list...
        if new_pos != False:
            self.grid_pos = new_pos[:]
            self.moved = True
        else:
            self.moved = False

        self.power -= 1

    def draw(self, screen, width, height):
        saturation = float(self.power) / self.max_pow * 255
        if saturation < 0:
            saturation = 0
        playerrect = pygame.Rect(self.grid_pos[0] * width / 16, \
            self.grid_pos[1] * height / 9, width / 16, height / 9)

        pygame.draw.rect(screen, (255 - saturation, saturation, 0), playerrect)

    def reset(self, power):
        self.grid_pos = self.init_pos[:]
        self.power = power
        self.max_pow = power

    def get_pos(self):
        return self.grid_pos
