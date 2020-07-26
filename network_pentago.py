#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pentago network
"""

from network import Network
from pentago import Pentago, grid
from itertools import product

class NetworkPentago(Network):
    """ pentago network """
    def __init__(self):
        """ init """
        super(NetworkPentago, self).__init__([36 * 2] + [72] * 1 + [36 + 4 * 2])
        self.nb_win = 0
        self.nb_lose = 0

    def forward(self, pentago):
        """ forward
            input are booléan !

            ==enemy_position===/36===|----|==out_position==/36==[filter]=[max]--
                                     | NW |
            ====our_position===/36===|----|==quad&rotation=/2*4==========[max]--

        """
        # process input
        enemy_state = [pentago.getpoint(x, y) == (not pentago.player)
                       for x, y in grid(6, 6)]
        our_state = [pentago.getpoint(x, y) == (pentago.player)
                     for x, y in grid(6, 6)]

        # compute forward
        nw_in = enemy_state + our_state
        nw_out = super(NetworkPentago, self).forward(nw_in).y_pred

        # process output
        outpos = lambda x, y: (nw_out[y*6+x] \
                               if pentago.getpoint(x, y) == pentago.VOID
                               else -float('Inf'))  # reject invalid pos
        x, y = max(grid(6, 6), key=lambda pos: outpos(*pos))
        quad, rot = max(grid(4, 2), key=lambda qr: nw_out[qr[0]*2+qr[1]]+36)
        return x, y, quad, rot

    def loss(self):
        """ let's maximize the victories """
        #return self.nb_lose / self.nb_win
        return "NOP"

    def winrate(self):
        """ winrate """
        if self.nb_win == 0:
            return 0
        return self.nb_win / (self.nb_win + self.nb_lose)

    def play(self, other, debug=False):
        """
        Play a game of pentago between the two networks.
        It is possible to realize only one game.
        """
        networks = (self, other, None)
        game = Pentago()
        while game.run:
            if debug:
                print(game)
            cmd = networks[game.player].forward(game)
            if debug:
                print("x={} y={} quad={} sens={}".format(*cmd))
            game.play(*cmd)
        if debug:
            print(game)
            print("winner is " + str(game.winner))
            print("with " + str(game.winpos))
        if game.winner != Pentago.VOID:
            networks[game.winner].nb_win += 1
            networks[not game.winner].nb_lose += 1
        return networks[game.winner]


    def __mod__(self, other):
        """ wn1 % nw2 => winner NW """
        assert type(self) == type(other)
        return self.play(other)

def playgame(nw_white, nw_black, debug=False):
    """
    Play game btw 2 nw
    """


def main():
    """ test """
    networks = (NetworkPentago(), NetworkPentago())
    winner = playgame(*networks, debug=True)
    print(winner)


if __name__ == '__main__':
    main()
