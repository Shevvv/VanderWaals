import sys
import pygame as pg
from iodine import Iodine
import settings as s


class App:

    pg.init()
    font = pg.font.SysFont(s.font, s.fontsize, bold=s.fontbold)
    efont = pg.font.SysFont(s.font, s.efontsize, bold=s.fontbold)
    clock = pg.time.Clock()

    def __init__(self):
        self.screen = pg.display.set_mode(s.screen_res)
        self.iodines = []
        self.pause = False

        self.funcs = {
            'exit': {
                'cases': [
                    {'type': pg.QUIT},
                    {'type': pg.KEYDOWN, 'key': pg.K_q},
                    {'type': pg.KEYDOWN, 'key': pg.K_ESCAPE},
                ],
                'method': self.exit
            },
            'next_phase': {
                'cases': [
                    {'type': pg.KEYDOWN, 'key': pg.K_RIGHT},
                    {'type': pg.MOUSEBUTTONDOWN},
                ],
                'method': self.next
            },
            'pause': {
                'cases': [
                    {'type': pg.KEYDOWN, 'key': pg.K_SPACE},
                ],
                'method': self.change_pause
            },
        }

        self.phase = 0
        self.phases = [
            self.make_iodine,
            self.add_electrons,
            self.move_electrons,
            self.add_dipole,
            self.exit
        ]

    def change_pause(self):
        self.pause = not self.pause

    def make_iodine(self):
        self.iodines.append(Iodine(self.screen, self.font, self.efont))

    def add_electrons(self):
        for iodine in self.iodines:
            iodine.add_electrons()

    def move_electrons(self):
        for iodine in self.iodines:
            iodine.move_electrons()

    def add_dipole(self):
        for iodine in self.iodines:
            iodine.add_dipole()

    def next(self):
        self.phases[self.phase]()
        self.phase += 1

    def update(self):
        if not self.pause:
            for iodine in self.iodines:
                iodine.update()

    def draw(self):
        self.screen.fill('black')

        for iodine in self.iodines:
            iodine.draw()

        pg.display.flip()

    def match_event(self, event):
        e_dict = {'type': event.type}
        if e_dict['type'] in (pg.KEYDOWN, pg.KEYUP):
            e_dict['key'] = event.key
        for func in self.funcs.values():
            if e_dict in func['cases']:
                return func['method']
        return self.pass_method

    @staticmethod
    def exit():
        pg.quit()
        sys.exit()

    @staticmethod
    def pass_method():
        pass

    def run(self):
        while True:
            for event in pg.event.get():
                self.match_event(event)()

            pg.display.set_caption(str(self.clock.get_fps()))
            self.update()
            self.draw()
            self.clock.tick(s.fps)


app = App()
app.run()
