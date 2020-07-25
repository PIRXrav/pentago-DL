#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pentago.py
"""

from itertools import product
from math import floor
import numpy as np


grid = lambda x, y: product(range(x), range(y))

winpos = [tuple(((x + i, y + 0) for i in range(5))) for x, y in grid(2, 6)]
winpos += [tuple(((x + 0, y + i) for i in range(5))) for x, y  in grid(6, 2)]
winpos += [tuple(((x + i, y + i) for i in range(5))) for x, y  in grid(2, 2)]
winpos += [tuple(((x + i, 5 - (y + i)) for i in range(5)))
           for x, y  in grid(2, 2)]

class Pentago:
    """ Pentago game """

    WHITE = 0
    BLACK = 1
    VOID = 2

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
        self.board = [np.full((3, 3), self.VOID) for _ in range(4)]
        self.player = self.WHITE  # white begin
        self.run = True  # game end ?
        self.cpt = 0 # nb of marble set
        self.winner = self.VOID # nobody
        self.winpos = ()

    def rotate(self, index_quadrant, sens):
        """ rotate quadrant [0; 3] """
        self.board[index_quadrant] = \
            np.rot90(self.board[index_quadrant], 1 if sens else 3)
        return self

    def setpoint(self, px, py, value):
        """ add point [0, 5] X [0, 5] """
        assert self.getpoint(px, py) == self.VOID
        self.board[floor(px / 3) + floor(py / 3) * 2][py % 3][px % 3] = value
        self.cpt += 1
        return self

    def getpoint(self, px, py):
        """ get point [0, 5] X [0, 5] """
        return self.board[floor(px / 3) + floor(py / 3) * 2][py % 3][px % 3]

    def play(self, posx, posy, quad, sens):
        """ play a turn """
        self.setpoint(posx, posy, self.player).rotate(quad, sens).check_win()
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
                if self.winpos and (px, py) in self.winpos:
                    ret += "\33[91m"
                ret += syms[self.getpoint(px, py)] + "\33[39m"
            ret += '\n'
        return ret

    def check_win(self):
        """ check if player win """
        if self.cpt == 36: # EOG
            self.run = False
        else:
            winner = [None for _ in (self.WHITE, self.BLACK, self.VOID)]
            for pos_tup in winpos:
                player = self.getpoint(*pos_tup[0])
                if sum(player == self.getpoint(*pos) for pos in pos_tup) == 5:
                    winner[player] = pos_tup

            self.run = not (winner[self.WHITE] or winner[self.BLACK])
            if not self.run:
                if winner[self.WHITE] and winner[self.BLACK]:
                    self.winner = self.VOID
                    self.winpos = (*winner[self.WHITE], *winner[self.BLACK])
                elif winner[self.WHITE]:
                    self.winner = self.WHITE
                    self.winpos = winner[self.WHITE]
                else:
                    self.winner = self.BLACK
                    self.winpos = winner[self.BLACK]
        return self.run

if __name__ == '__main__':
    for poss in winpos:
        game = Pentago()
        for pos in poss:
            game.setpoint(*pos, game.BLACK)
        print(poss)
        print(game)
