# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS


db = pymysql.connect("wangzan-db.mysql.polardb.singapore.rds.aliyuncs.com","wangzan","123@qweASD","myfavorite")
cursor = db.cursor

cursor.execute("select id,username,role,ctime from login")

data = cursor.fetchall()
print(data)