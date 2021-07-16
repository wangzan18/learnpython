# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS


connection = pymysql.connect(host="wangzan-db.mysql.polardb.singapore.rds.aliyuncs.com",
                     user="wangzan",
                     password="123@qweASD",
                     db="myfavorite",
                     cursorclass=pymysql.cursors.DictCursor)
               
                     
with connection.cursor() as cursor:
    sql = "select id,username,role,ctime from login"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)