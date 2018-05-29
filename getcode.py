#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
import re

def checkWORK(sid, sdirname, path="test"):
    try:
        path = path + "/" + str( sid ) + "/" + sdirname
        with open(path + "/work.py") as f: # type(lines) = list()
            # code = "".join(lines)
            lines = f.readlines()
            lines = [re.sub("\'", "\"", line) for line in lines]
            # 计算行数,并且除去空白行数
            len_thecode = [line for line in lines if line != '\n' and line != '    \n']
            len_code = len(len_thecode)
            lines = "".join(lines)
            data = {
                    "code": lines,
                    "lencode": len_code
                    }
            return data
    except:
        print("error")

if __name__ == "__main__":
    a = checkWORK(sid=15080930213, sdirname="heihei")
    pprint(a)
