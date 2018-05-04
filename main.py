#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3
from multiprocessing import Pool

class MAIN:

    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect("class.db",check_same_thread = False)
        cur = self.db.execute("select sid from students")
        self.data = [row[0] for row in cur.fetchall()]

    # 创建文件夹
    def createDIR(self, filename):
        data = self.data
        for row in data:
            path = self.path + "/" + str( row ) + "/" + filename
            os.system("cp -rf moudle %s"%(path))
            print("create dir %s"%(path))

    # 删除作业
    def delWork(self, filename):
        data = self.data
        for row in data:
            path = self.path + "/" + str( row ) + "/" + filename
            os.system("rm -rf %s"%(path))
            print("delete dir %s"%(path))

if __name__ == "__main__":
    m = MAIN("test")
    m.delWork("ddd")
