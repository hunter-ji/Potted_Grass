#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from pprint import pprint

lines = os.popen("pytest -s test_work.py").readlines()
line = [line for line in lines if line != ""]
print("".join(line))
