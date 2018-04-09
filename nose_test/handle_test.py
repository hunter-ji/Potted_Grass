#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

lines = os.popen("nosetests -s test_work.py").readlines()
for line in lines:
    print()
