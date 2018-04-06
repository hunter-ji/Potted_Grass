#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import json
import time
import re

# 存储运行的数据
# Data = {
#         "0":{
#           ... 
#             },
#         "1":{
#           ...
#             }
# }
def handle(work_id, sid, result):
    db = sqlite3.connect("class.db",check_same_thread = False)
    cur = db.execute("select content from status where work_id = ? and sid = ?",[work_id, sid])
    data = [row[0] for row in cur.fetchall()]
    if data == ["info"]:
        Data = {}
        Data['1'] = result
        db.execute('update status set content = ? where work_id = ? and sid = ?',[str(Data), work_id, sid])
        db.execute("update status set status = ? where work_id = ? and sid = ?",[int( result["info"]), work_id, sid])
        db.commit() 
        db.close()
    else:
        data = re.sub("\'", "\"", data[0])
        data = json.loads(data)
        data[str(len(data.keys()) + 1)] = result
        db.execute("update status set content = ? where work_id = ? and sid = ?",[str(data), work_id, sid])
        db.execute("update status set status = ? where work_id = ? and sid = ?",[int( result["info"] ), work_id, sid])
        db.commit()
        db.close()
    return "ok"

# 运行处理目标函数
def checkWORK(work_id, path, sid, filename):
    path = path + "/" + str( sid ) + "/" + filename
    sys.path.append(path)
    logtime = time.strftime('%Y-%m-%d %H:%M:%S')
    #　当函数不存在的时候
    try:
        from work import heihei
    except:
        result = {
                "info": "0",
                "message": "函数不存在",
                "time": logtime
                }
        return handle(work_id, sid, result)
    # 当函数运行成功和不成功的时候
    try:
        r = heihei()
        result = {
                "info": "2",
                "message": "函数运行成功",
                "result": r,
                "time": logtime
                }
        return handle(work_id, sid, result)
    except:
        info = sys.exc_info()
        # 报错
        error = info[1]
        error = str(error).replace(",", "")
        error = str(error).replace("\"", " ")
        error = str(error).replace("\'", " ")
        error = re.sub("\'", "\"", error)
        with open(path + "/work.py") as f: # type(lines) = list()
            # code = "".join(lines)
            lines = f.readlines() 
            lines = [re.sub("\'", "\"", line) for line in lines]
            lines = [re.sub("\:", "\\\:", line) for line in lines]
            lines = "".join(lines)
        result = {
                "info": "1",
                "message":"函数运行错误",
                "error":error,
                "code":lines,
                "time": logtime
                }
        return handle(work_id, sid, result)

if __name__ == "__main__":
    checkWORK(1, "test", 15080930211, "heihei")
