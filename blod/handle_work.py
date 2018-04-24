#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from pprint import pprint

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
if result == "failed":
    print("失败")
    print("失败原因如下:")
    outputs = [L[i] for i in L if i > 11 and i < (len(L)-2)]
    print("\n".join(outputs))
    log = [row[8:] for row in outputs if "E" in row]
    print("错误信息", "".join(log))
elif result == "passed":
    print("成功")
    L2 = {v: k for k, v in L.items()}
    outputs = [L[i].replace("test_work.py ", "") for i in L if i > 4 and i < L2["."]]
    print("输出分别为:")
    print("\n".join(outputs))
elif result == "error":
    print("错误")
    print("错误信息如下:")
    outputs = [L[i] for i in L if i > 6 and i < (len(L)-2)]
    log = [row[8:] for row in outputs if "E" in row]
    print("\n".join(outputs))
    print("错误信息", "".join(log))
