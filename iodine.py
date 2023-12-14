import pygame as pg
import settings as s
from electron import Electron
from dipole import Dipole


class Iodine:

    def __init__(self, screen, font, efont):
        self.screen = screen
        self.font = font
        self.efont = efont
        self.electrons = []
        self.dipole = None

        # set up the rectangle and its position
        self.rect = pg.Rect(0, 0,
                            s.iodine_width, s.iodine_height)
        self.centera = -s.iodine_width // 4, 0
        self.centerb = s.iodine_width // 4, 0
        self.rect.centerx = self.screen.get_width() // 2
        self.rect.centery = self.screen.get_height() // 2

        # set up the text
        self.text = self.font.render('+', True, 'red')
        self.text_coords = []
        self.text_width, self.text_height = self.text.get_width(), \
                                            self.text.get_height()
        self.text_pos()

    def add_electrons(self):
        for i in range(2):
            pos = 0, s.electron_start_offset * (2 * i - 1)
            self.electrons.append(Electron(self, pos, self.screen, self.efont))
        self.dipole = Dipole(self, self.screen)

    def move_electrons(self):
        for electron in self.electrons:
            electron.static = False

    def add_dipole(self):
        self.dipole.activate()

    def update(self):
        self.text_pos()
        for electron in self.electrons:
            electron.update()

        if self.dipole:
            self.dipole.update()

    def text_pos(self):
        for coords in (self.centera, self.centerb):
            text_coords_x = coords[0] - self.text_width // 2
            text_coords_y = coords[1] - self.text_height // 2
            self.text_coords.append((text_coords_x, text_coords_y))

    def rel_to_abs(self, coords):
        return self.rect.centerx + coords[0], self.rect.centery + coords[1]

    def draw(self):
        # pg.draw.rect(self.screen, 'green', self.rect)
        if self.dipole:
            self.dipole.draw()

        for coords in (self.centera, self.centerb):
            pg.draw.circle(self.screen, s.iodine_color,
                           self.rel_to_abs(coords),
                           int(s.size_mod * self.text_height // 2))
        for coords in self.text_coords:
            self.screen.blit(self.text, self.rel_to_abs(coords))

        for electron in self.electrons:
            electron.draw()
