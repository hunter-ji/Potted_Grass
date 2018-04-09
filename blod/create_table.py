#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('class.db')
print ( "Opened database successfully!" )
# 管理者
conn.execute('''
create table users(
id integer primary key autoincrement,
username char(8),
content blob
);''')
print ( "Table created successfully!" )
