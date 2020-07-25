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
        super(NetworkPentago, self).__init__([36 * 2] + [72] * 2 + [36 + 4 * 2])

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
        quad, rot = max(grid(4, 2), key=lambda qr: nw_out[qr[0]*2+qr[1]])
        return x, y, quad, rot

def main():
    """ test """
    networks = [NetworkPentago(), NetworkPentago()]
    game = Pentago()
    while game.run:
        print(game)
        cmd = networks[game.player].forward(game)
        print("x={} y={} quad={} sens={}".format(*cmd))
        game.play(*cmd)
    print(game)
    print("winner is " + str(game.winner))
    print("with " + str(game.winpos))

if __name__ == '__main__':
    main()
