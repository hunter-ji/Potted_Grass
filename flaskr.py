#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, g, redirect, url_for, \
     abort, render_template, flash, json, jsonify, session
import os
import sqlite3
import re
import time
from multiprocessing import Pool
from main import MAIN
from handle import checkWORK

DATABASE = 'class.db'
SECRET_KEY = os.urandom(24)

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.commit()
    g.db.close()

# 首页
@app.route("/")
def index():
    if not session.get('logged_in'):
        return redirect("login")
    cur = g.db.execute("select * from works order by id desc limit 3")
    data = [dict(id=row[0], name=row[1], filename=row[2], time=row[3]) for row in cur.fetchall()]
    return render_template("index.html", data=data)

# 获取每次作业情况
@app.route("/table/<int:wid>/", methods=["GET", "POST"])
def table(wid):
    if not session.get('logged_in'):
        return redirect("login")
    works = g.db.execute("select * from students")
    works = [dict(id=row[0], sid=row[1], name=row[2]) for row in works.fetchall()]

    statuss = g.db.execute("select sid, status, content from status where work_id = ?",[wid])
    statuss = [dict(sid=row[0], status=row[1], content=row[2]) for row in statuss.fetchall()]
#    statuss = [dict( row["sid"]=row["status"] ) for row in statuss]
    statuss1 = {}
    statuss2 = {}
    for row in statuss:
        statuss1[row["sid"]] = row["status"]
        statuss2[row["sid"]] = row["content"]
    data = []
    for info in works:
        status = str(statuss1[info["sid"]])
        if status == "0":
            d = "<p class='text-danger'>文件不存在</p>"
        elif status == "1":
            d = "<p class='text-warning'>运行错误</p>"
        elif status == "2":
            result = statuss2[info["sid"]]
            result = re.sub("\'", "\"", result)
            result = json.loads(result)
            result = result[str( len(result.keys()) )]["result"]
            d = "输出 : %s</p>"%(str(result))
        else:
            d = "未检查"
        details = "<a target='_black' href='/details/%s/%s/'>%s</a>"%(str(wid), str(info["sid"]), d)
        info["details"] = details
        data.append(info)
#      data = [
            #  {
                #  "id": "0",
                #  "sid": "15080930211",
                #  "name": "kuari",
                #  "details": "<a target='_black' href='/details/1/15080930211/'>details</a>"
                #  }
#      ]
    return jsonify(data)

# 发布作业
@app.route("/issuetask/", methods=["POST"])
def issuetask():
    if not session.get('logged_in'):
        return redirect("login")
    name = request.form["name"]
    filename = request.form["filename"]
    logtime = time.strftime('%Y-%m-%d %H:%M:%S')
    g.db.execute("insert into works (name, filename, time) values (?, ?, ?)", [name, filename, logtime])
    g.db.commit()
    cur = g.db.execute("select sid from students")
    MAIN("test").createDIR(filename)

    # 拿到作业id
    cur2 = g.db.execute("select id from works where name = ?",[name])
    data = int( [row[0] for row in cur2.fetchall()][0] )
    # 拿到学号
    cur3 = g.db.execute("select sid from students")
    sids = [row[0] for row in cur.fetchall()]
    for sid in sids:
        g.db.execute("insert into status (work_id, sid, status, content) values (?,?,?,?)",[data, sid, 3, "info"])
    g.db.commit()
    return redirect(url_for("index"))

# 名单
@app.route("/list/", methods=["GET"])
def list():
    if not session.get('logged_in'):
        return redirect("login")
    return render_template("list.html")

# 名单data
@app.route("/lists", methods=["GET"])
def lists():

    cur = g.db.execute("select * from students")
    content = [dict(sid=row[1], name=row[2]) for row in cur.fetchall()]
    return jsonify(content)

# 详情页面
@app.route("/details/<int:work_id>/<int:sid>/")
def details(work_id, sid):
    if not session.get('logged_in'):
        return redirect("login")
    cur = g.db.execute("select content from status where work_id = ? and sid = ?",[work_id, sid])
    data = [row[0] for row in cur.fetchall()]
#    if data == ["info"]:
    w = g.db.execute("select * from works where id = ?",[work_id])
    w = [dict(id=row[0], name=row[1], filename=row[2], time=row[3]) for row in w.fetchall()][0]
    s = g.db.execute("select * from students where sid = ?",[sid])
    s = [dict(id=row[0], sid=row[1], sname=row[2]) for row in s.fetchall()][0]
    content = g.db.execute("select content from status where work_id = ? and sid = ?",[work_id, sid])
    content = [row[0] for row in content.fetchall()][0]
#    content = re.sub("\'", "\"", content)
    data = json.loads(content)
    content = []
    for i in data:
        L = {} 
        L[i] = data[i]
        content.append(L)
    return render_template("details.html", w=w, s=s, content=content)
#    return redirect(url_for("index"))

# 登录
@app.route("/login/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        cur = g.db.execute("select username from users")    
        usernames = [row[0] for row in cur.fetchall()]
        cur2 = g.db.execute("select password from users where username = ?",[username])
        the_password = [row[0] for row in cur2.fetchall()][0]
        if username not in usernames:
            error = 'Invalid username'
        elif password != the_password:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

#　登出
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# 检查作业状态
@app.route("/handle", methods=["POST"])
def handle():
    data = request.get_data()
    theid = int(json.loads(data)['id'])

    works = g.db.execute("select filename from works where id = ?",[theid])
    filename = [row[0] for row in works.fetchall()][0]
    L = {}
    pool = Pool(processes = 20)
    sids = g.db.execute("select sid from students")
    sids = [row[0] for row in sids.fetchall()]
    for sid in sids:
        pool.apply_async(checkWORK, args=(theid, "test", sid, filename,))
    pool.close()
    pool.join()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
