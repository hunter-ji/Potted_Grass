#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from pprint import pprint

def output(result):
    pass

lines = os.popen("pytest -s test_work.py").readlines()
line = [line for line in lines if line != ""]
print("".join(line))
print("++++++"*10)
i = 0
L = {}
for line in lines:
    line = line.replace("\n", "")
    line = line.replace("=", "")
    L[i] = line
    i += 1
pprint(L)

print("###"*10)

l = len(L)
result = L[l-1][3:-17]
print(result)
