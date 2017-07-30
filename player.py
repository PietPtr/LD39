import pygame
import time

MOVETIME = 0.144 # s

class Player(object):
    def __init__(self, grid_position, power):
        self.grid_pos = grid_position
        self.init_pos = grid_position
        self.power = power
        self.max_pow = power
        self.moved = False
        self.last_move_time = time.time()
        self.last_move = [0, 0]

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

        if direction != [0, 0]:
            self.power -= 1

        if new_pos != False:
            self.grid_pos = new_pos[:]
            self.moved = True
            self.last_move_time = time.time()
            self.last_move = direction[:]
        else:
            self.moved = False

        # print (self.max_pow - self.power)

    def draw(self, screen, width, height):
        saturation = float(self.power) / self.max_pow * 255
        if saturation < 0:
            saturation = 0


        # playerrect = pygame.Rect(self.grid_pos[0] * width / 16, \
        #     self.grid_pos[1] * height / 9, width / 16, height / 9)
        #
        # pygame.draw.rect(screen, (50, 50, 50), playerrect)




        time_since_move = time.time() - self.last_move_time
        if time_since_move > MOVETIME:
            time_since_move = MOVETIME


        x = (self.grid_pos[0] - self.last_move[0]) * width / 16 + (width / 16) \
                * time_since_move * 1 / MOVETIME * self.last_move[0]
        y = (self.grid_pos[1] - self.last_move[1]) * height / 9 + (height / 9) \
                * time_since_move * 1 / MOVETIME * self.last_move[1]

        playerrect = pygame.Rect(x, y, width / 16, height / 9)

        pygame.draw.rect(screen, (255 - saturation, saturation, 79), playerrect)

        batwidth = 0.4
        batheight = 0.7
        batcolor = (41, 43, 44)
        batpower = self.power
        if batpower < 0:
            batpower = 0

        #batx = x + width / 16 * batwidth - width / 16 / 4
        batx = x + width / 16 / 2 - (width / 16) * batwidth / 2
        baty = y + height / 9 / 2 - (height / 9) * batheight / 2

        fillheight = height / 9 * batheight * (batpower / self.max_pow)
        batfillrect = pygame.Rect(batx, baty + (height / 9 * batheight - fillheight), width / 16 * batwidth, fillheight)

        pygame.draw.rect(screen, batcolor, batfillrect)

        batrect = pygame.Rect(batx, baty, width / 16 * batwidth, height / 9 * batheight)

        pygame.draw.rect(screen, batcolor, batrect, 2)


    def reset(self, power):
        self.grid_pos = self.init_pos[:]
        self.power = power
        self.max_pow = power

    def get_pos(self):
        return self.grid_pos
