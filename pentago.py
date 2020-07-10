#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pentago.py
"""

from math import floor
import numpy as np


class Pentago:
    """ Pentago game """

    def __init__(self):
        """ init """
        #
        #     0 | 1
        #   --------
        #     2 | 3
        #
        # 2: void
        # 0: white
        # 1: black
        self.WHITE = 0
        self.BLACK = 1
        self.VOID = 2
        self.board = [np.full((3, 3), self.VOID) for _ in range(4)]
        self.player = self.WHITE  # white begin
        self.run = True  # game end ?

    def rotate(self, index_quadrant, sens):
        """ rotate quadrant [0; 3] """
        self.board[index_quadrant] = \
            np.rot90(self.board[index_quadrant], 1 if sens else 3)

    def setpoint(self, px, py, value):
        """ add point [0, 5] X [0, 5] """
        assert self.getpoint(px, py) == self.VOID
        self.board[floor(px / 3) + floor(py / 3) * 2][py % 3][px % 3] = value

    def getpoint(self, px, py):
        """ get point [0, 5] X [0, 5] """
        return self.board[floor(px / 3) + floor(py / 3) * 2][py % 3][px % 3]

    def play(self, posx, posy, quadrant, sens):
        """ play a turn """
        self.setpoint(posx, posy, self.player)
        self.rotate(quadrant, sens)
        self.player = 1 - self.player

    def __str__(self):
        """ display board """
        syms = ['X', 'O', '.']
        ret = ""
        for py in range(6):
            if py == 3:
                ret += '---+---\n'
            for px in range(6):
                if px == 3:
                    ret += '|'
                ret += syms[self.getpoint(px, py)]
            ret += '\n'
        return ret

    def __eq__(self, other):
        return self.run == other
