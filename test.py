#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from main import foo


class TestMain(unittest.TestCase):
    """ Test foo """

    def setUp(self):
        self.i1 = 10
        self.b = 5

    def test_foo(self):
        result = foo(1)
        self.assertEqual(foo(1), 2)


def suite():
    """ Test suite """
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMain))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
