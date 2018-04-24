#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import imp
path = sys.argv[2]
w = imp.load_source('work', path+'/work.py')
def test_work():
    assert w.heihei() == 'test'