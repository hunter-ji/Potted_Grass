#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import base64
import sqlite3
import json
import re
from pprint import pprint

def de(line):
    return base64.b64encode(line.encode("utf-8")).decode()

def handle(wid, sid, result):
    db = sqlite3.connect("class.db",check_same_thread = False)
    cur = db.execute("select content from status where wid = ? and sid = ?",[wid, sid])
    data = [row[0] for row in cur.fetchall()]
    if data == ["info"]:
        Data = {}
        Data['1'] = result
        db.execute('update status set content = ? where wid = ? and sid = ?',[str(Data), wid, sid])
        db.execute("update status set status = ? where wid = ? and sid = ?",[int( result["info"]), wid, sid])
        db.commit()
        db.close()
    else:
        data = re.sub("\'", "\"", data[0])
        data = json.loads(data)
        data[str(len(data.keys()) + 1)] = result
        db.execute("update status set content = ? where wid = ? and sid = ?",[str(data), wid, sid])
        db.execute("update status set status = ? where wid = ? and sid = ?",[int( result["info"] ), wid, sid])
        db.commit()
        db.close()
    return "ok"

def checkWORK(wid, path, sid, sdirname):
    logtime = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        path = path + "/" + str( sid ) + "/" + sdirname
        # pytest -s test_work.py path
        cmd = "pytest check/test_work%s.py %s -s"%(wid, path)
        lines = os.popen(cmd).readlines()
        line = [line for line in lines if line != ""]
        i = 0
        L = {}
        for line in lines:
            line = line.replace("\n", "")
            line = line.replace("=", "")
            L[i] = line
            i += 1
        l = len(L)
        result = L[l-1][3:-17]
        # 读取代码
        with open(path + "/work.py") as f: # type(lines) = list()
            # code = "".join(lines)
            lines = f.readlines()
            lines = [re.sub("\'", "\"", line) for line in lines]
            # 计算行数,并且除去空白行数
            len_thecode = [line for line in lines if line != '\n' and line != '    \n']
            len_code = len(len_thecode)
            lines = "".join(lines)
            lines = base64.b64encode(lines.encode("utf-8")).decode()
        if result == "failed":
            outputs = [L[i] for i in L if i > 11 and i < (len(L)-2)]
            result = "\n".join(outputs)
            log = [row[8:] for row in outputs if "E" in row]
            message = "".join(log)
            message = re.sub("\'", "\"", message)

            results = {
                    "info": "1",
                    "message": de(message),
                    "result": de(result),
                    "code": de(lines),
                    "lencode": str(len_code),
                    "time": logtime
            }
    #        return results
            return handle(wid, sid, results)
        elif result == "passed":
            message = "运行成功"
            L2 = {v: k for k, v in L.items()}
            ss = "check/test_work%s.py "%(wid)
            if "." in L2:
                outputs = [L[i].replace(ss, "") for i in L if i > 4 and i < L2["."]]
            else:
                outputs = [L[i].replace(ss, "") for i in L if i > 4]
            result = "\n".join(outputs)
            if "passed" in result and "seconds" in result:
                result = "无输出"

            results = {
                    "info": "2",
                    "message": de(message),
                    "result": de(result),
                    "code": de(lines),
                    "lencode": str(len_code),
                    "time": logtime
            }
    #        return results
            return handle(wid, sid, results)
        elif result == "error":
            outputs = [L[i] for i in L if i > 6 and i < (len(L)-2)]
            log = [row[4:] for row in outputs if "E " in row]
            result = "\n".join(outputs)
            message = "".join(log)
            message = re.sub("\'", "\"", message)

            results = {
                    "info": "0",
                    "message": de(message),
                    "result": de(result),
                    "code": de(lines),
                    "lencode": str(len_code),
                    "time": logtime
            }
    #        return results
            return handle(wid, sid, results)
    except:
        results = {
                "info": "3",
                "message": de("no file"),
                "result": de("no file"),
                "time": logtime
        }
        return handle(wid, sid, results)

if __name__ == "__main__":
    a = checkWORK(3, "test", 15080930213, "hehe")
    pprint(a)
