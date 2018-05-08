#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('class.db')
print ( "Opened database successfully!" )

# 名单
conn.execute('''
create table students(
id integer primary key autoincrement,
sid  int,
sname char(4),
sclass char(7)
);''')

# 管理者
conn.execute('''
create table users(
id integer primary key autoincrement,
username char(8),
password char(10)
);''')

# 作业
conn.execute('''
create table works(
id integer primary key autoincrement,
name char(20),
filename char(10),
time char(20)
);''')

# 作业状态
conn.execute('''
create table status(
id integer primary key autoincrement,
wid int,
sid int,
status int,
content text
);''')

print ( "Table created successfully!" )
