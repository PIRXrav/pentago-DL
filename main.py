#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pentago import Pentago


def get_play_cmd():
    try:
        print("x[0, 5]\ny[0, 5]\nquad[0, 3]\nsens[0, 1]")
        dat = tuple([int(input()) for _ in range(4)])
        assert 0 <= dat[0] <= 5
        assert 0 <= dat[1] <= 5
        assert 0 <= dat[2] <= 3
        assert 0 <= dat[3] <= 1
        print("x={} y={} quad={} sens={}".format(*dat))
        return dat
    except:
        print("Error entry")


if __name__ == '__main__':
    game = Pentago()
    print(game)
    while game:
        game.play(*get_play_cmd())
        print(game)
