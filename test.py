#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test module
"""
import unittest
from pentago import Pentago


class TestPentago(unittest.TestCase):
    """ Test pentago """

    def setUp(self):
        pass

    def test_init(self):
        """ test init """
        game = Pentago()
        str(game)
        for y in range(6):
            for x in range(6):
                self.assertEqual(game.getpoint(x, y), game.VOID)

    def test_set_get(self):
        """ test set get """
        mat = [[1, 2, 1, 1, 1, 1],
               [1, 1, 1, 0, 0, 0],
               [1, 1, 1, 0, 0, 0],
               [0, 1, 1, 0, 2, 0],
               [0, 1, 1, 0, 2, 0],
               [0, 1, 1, 0, 2, 0]]

        game = Pentago()
        # set
        for y, line in enumerate(mat):
            for x, value in enumerate(line):
                if value != game.VOID:
                    game.setpoint(x, y, value)
        # get
        for y, line in enumerate(mat):
            for x, value in enumerate(line):
                self.assertEqual(game.getpoint(x, y), value)

    def test_rotate(self):
        """ test rotate """
        game = Pentago()
        # init
        game.setpoint(0, 0, 1)
        self.assertEqual(game.getpoint(0, 0), 1)
        # rotate
        game.rotate(0, 1)  # trigo
        self.assertEqual(game.getpoint(0, 2), 1)
        self.assertEqual(game.getpoint(0, 0), game.VOID)
        # rotate
        game.rotate(0, 0)  # anti trigo
        self.assertEqual(game.getpoint(0, 0), 1)
        self.assertEqual(game.getpoint(0, 2), game.VOID)

    def test_play(self):
        """ test play """
        game = Pentago()
        game.play(3, 0, 0, 1)
        self.assertEqual(game.getpoint(3, 0), game.WHITE)
        game.play(4, 1, 1, 0)
        self.assertEqual(game.getpoint(3, 0), game.VOID)
        self.assertEqual(game.getpoint(5, 0), game.WHITE)
        self.assertEqual(game.getpoint(4, 1), game.BLACK)


def gen_suite():
    """ gen tests suite """
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPentago))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(gen_suite())
