import settings as s
from psi import Psi
import pygame as pg
import numpy as np
import math


class Electron:

    psi = Psi()

    def __init__(self, iodine, pos, screen, font):
        self.iodine = iodine
        self.pos = pos
        self.screen = screen
        self.font = font

        self.static = True
        self.dirx = 0
        self.diry = 0
        self.randomize_direction()

        # set up the text
        self.text = self.font.render('-', True, 'white')
        self.text_x, self.text_y = 0, 0
        self.text_width, self.text_height = self.text.get_width(), \
                                            self.text.get_height()
        self.text_pos()

    def text_pos(self):
        self.text_x = self.pos[0] - self.text_width // 2
        self.text_y = self.pos[1] - \
                      self.text_height * (s.etext_offset + 1) // 2

    def compute_direction(self):
        abs_pos = self.iodine.rel_to_abs(self.pos)
        psi_vector = self.psi.norm_mo_cos[abs_pos[1]][abs_pos[0]],\
                     self.psi.norm_mo_sin[abs_pos[1]][abs_pos[0]]
        _psi_strength = self.psi.mo_psi[abs_pos[1]][abs_pos[0]]
        psi_strength = 1 - _psi_strength / self.psi.max_mo_psi
        self.dirx = psi_strength * psi_vector[0] + \
                    (1 - psi_strength) * self.dirx
        self.diry = psi_strength * psi_vector[1] + \
                    (1 - psi_strength) * self.diry
        norm = math.sqrt(self.dirx ** 2 + self.diry ** 2)
        self.dirx, self.diry = round(self.dirx / norm, 5),\
                               round(self.diry / norm, 5)

    def randomize_direction(self):
        self.dirx = np.random.uniform(-1, 1, None)
        self.diry = math.sqrt(1 - self.dirx ** 2)

    def update(self):
        if not self.static:
            self.compute_direction()
            if np.isnan(self.dirx) or np.isnan(self.diry):
                self.randomize_direction()

            self.pos = int(self.pos[0] + self.dirx * s.espeed),\
                       int(self.pos[1] + self.diry * s.espeed)

            self.text_pos()

    def draw(self):
        abs_pos = self.iodine.rel_to_abs(self.pos)
        pg.draw.circle(self.screen, 'blue', abs_pos, s.electron_radius)
        self.screen.blit(self.text,
                         self.iodine.rel_to_abs((self.text_x, self.text_y)))
