#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import sqlite3

db = sqlite3.connect("class.db",check_same_thread = False)

encoded = base64.b64encode(a)
print(encoded)
data = base64.b64decode(encoded)
print(data)
