from scipy.stats import lognorm
import numpy as np
import settings as s
import math


class Psi:

    def __init__(self):
        self.centera = s.iodine_width // 4
        self.centerb = -self.centera
        self.radius = s.psi_size * s.iodine_width * s.psi_scale / 4 / 6.8
        self.atom_psi_a, self.atom_psi_b = None, None
        self.mo_psi = []

        self.build_atom_psi()
        self.build_mo_psi()
        self.max_mo_psi = np.max(self.mo_psi)

        self.mo_sin, self.mo_cos = [], []
        self.norm_mo_sin, self.norm_mo_cos = [], []
        self.normalize_gradient()

    def build_atom_psi(self):
        a_distances = []
        b_distances = []
        for j in range(-s.psi_height, s.psi_height):
            a_row = []
            b_row = []
            for i in range(-s.psi_width, s.psi_width):
                diff_x_a, diff_x_b = self.centera - i, self.centerb - i
                diff_y_a, diff_y_b = -j, -j
                a_row.append(math.sqrt(diff_x_a ** 2 + diff_y_a ** 2))
                b_row.append(math.sqrt(diff_x_b ** 2 + diff_y_b ** 2))
            a_distances.append(a_row)
            b_distances.append(b_row)

        self.atom_psi_a = lognorm.pdf(a_distances, s=s.psi_sigma,
                                      loc=s.iodine_width * s.psi_size / 4,
                                      scale=s.psi_scale)
        self.atom_psi_b = lognorm.pdf(b_distances, s=s.psi_sigma,
                                      loc=s.iodine_width * s.psi_size / 4,
                                      scale=s.psi_scale)

    def build_mo_psi(self):
        for j, line in enumerate(self.atom_psi_a):
            row = []
            for i, cell in enumerate(line):
                row.append(cell + self.atom_psi_b[j][i])
            self.mo_psi.append(row)

    def normalize_gradient(self):
        dy, dx = np.gradient(self.mo_psi)
        for j, line in enumerate(dy):
            row_sin, row_cos = [], []
            for i, cell in enumerate(line):
                dxa, dxb = self.centera - i + s.screen_res[0] // 2,\
                           self.centerb - i + s.screen_res[0] // 2
                dya, dyb = s.screen_res[1] // 2 - j, s.screen_res[1] // 2 - j
                if (l := math.sqrt(dxa ** 2 + dya ** 2)) <= 0.4 * self.radius:
                    if l == 0:
                        l, dya, dxa = 1, 0, 1
                    row_sin.append(-dya / l), row_cos.append(-dxa / l)
                    self.mo_psi[j][i] = 0
                elif (l := math.sqrt(dxb ** 2 + dyb ** 2)) <= 0.4 * \
                        self.radius:
                    if l == 0:
                        l, dyb, dxb = 1, 0, -1
                    row_sin.append(-dyb / l), row_cos.append(-dxb / l)
                    self.mo_psi[j][i] = 0
                else:
                    norm = math.sqrt(cell ** 2 + dx[j, i] ** 2)
                    row_sin.append(cell / norm), row_cos.append(dx[j, i] / norm)
            self.norm_mo_sin.append(row_sin), self.norm_mo_cos.append(row_cos)
        self.norm_mo_sin, self.norm_mo_cos = np.array(self.norm_mo_sin), \
                                             np.array(self.norm_mo_cos)
