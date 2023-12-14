import math
import pygame as pg
import settings as s


class Dipole:

    def __init__(self, iodine, screen):
        self.iodine = iodine
        self.screen = screen
        self.points = None
        self.show = False

    def activate(self):
        self.show = True

    def deactivate(self):
        self.show = False

    def find_direction(self):
        poss = []
        for electron in self.iodine.electrons:
            poss.append(electron.pos)
        x = (poss[0][0] + poss[1][0]) / 2
        y = (poss[0][1] + poss[1][1]) / 2
        return x, y

    def find_points(self):
        direction = self.find_direction()
        antipode = (-direction[0], -direction[1])
        length = math.sqrt((direction[0] - antipode[0]) ** 2 +
                           (direction[1] - antipode[1]) ** 2)

        if direction[0] - antipode[0] == 0:
            p_k = 0
        elif direction[1] - antipode[1] == 0:
            p_k = None
        else:
            k = (direction[1] - antipode[1]) / (direction[0] - antipode[0])
            p_k = -1 / k

        if p_k:
            dx = s.arrow_width * length / math.sqrt(1 + p_k ** 2)
            dy = p_k * dx
        else:
            dx = 0
            dy = s.arrow_width * length

        end1, end2 = (antipode[0] - dx, antipode[1] - dy),\
                     (antipode[0] + dx, antipode[1] + dy)

        headpoint = direction[0] * s.head, direction[1] * s.head
        hp1, hp2, hp3, hp4 = (headpoint[0] - 2 * dx, headpoint[1] - 2 * dy),\
                             (headpoint[0] - dx, headpoint[1] - dy),\
                             (headpoint[0] + dx, headpoint[1] + dy), \
                             (headpoint[0] + 2 * dx, headpoint[1] + 2 * dy)

        points = end1, end2, hp3, hp4, direction, hp1, hp2
        to_return = []
        for point in points:
            to_return.append(self.iodine.rel_to_abs(point))
        return to_return

    def update(self):
        self.points = self.find_points()

    def draw(self):
        if self.show:
            pg.draw.polygon(self.screen, s.arrow_color, self.points)
