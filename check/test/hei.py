#!/usr/bin/python
# -*- coding: utf-8 -*-
def heihei():
    with open("ttt.txt", "r") as f:
        aa = f.read()
        print(aa)
    return "test"

if __name__ == "__main__":
    heihei()
