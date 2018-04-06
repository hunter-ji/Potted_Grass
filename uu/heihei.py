#!/usr/bin/python
# -*- coding: utf-8 -*-
from work import hei
import unittest

class TestDict(unittest.TestCase):

    def test_key(self):
        self.assertSetEqual(hei(1), 2)

if __name__ == "__main__":
    unittest.main()

