#!/usr/bin/python
# -*- coding: utf-8 -*-
adict = {
            1:"a",
            2:"b",
            3:"c"
        }

def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

a = sorted(dict2list(adict), key=lambda x:x[1], reverse=True) # 按照第1个元素降序排列

print(a)
L = {}
for i in a:
    print(i)
    L[i[0]] = i[1]

print(L)
