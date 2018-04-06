#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os

db = sqlite3.connect("class.db",check_same_thread = False)

for id in range(1,9):
    sid = "1508093021" + str(id)
    sname = "同学" + str(id)
    db.execute("insert into students (sid, sname) values (?,?)",[sid, sname])
    db.commit()


for id in range(1,9):
    sid = "1508093021" + str(id)
    try:
        os.mkdir("../test/%s"%sid)
        print ("创建文件夹%s成功"%sid)
    except:
        print ("创建文件夹%s失败"%sid)
