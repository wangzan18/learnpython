# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS


connection = pymysql.connect(host="wangzan-db.mysql.polardb.singapore.rds.aliyuncs.com",
                     user="wangzan",
                     password="123@qweASD",
                     db="myfavorite",
                     cursorclass=pymysql.cursors.DictCursor)


#后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/user/list', methods=['POST'])
def user_list():
    if request.method == "POST":
        with connection.cursor() as cursor:
            sql = "select id,username,role,ctime from login"
            cursor.execute(sql)
            result = cursor.fetchall()
        if request != None:
            print(result)
            return jsonify(result)


@app.route('/user/add', methods=['POST'])
def user_add():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            role = int(request.form.get('role'))
            with connection.cursor() as cursor:
                sql = "insert into login(username, password, role) values (%s, %s, role)"
                cursor.execute(sql, (username, password))
            connection.commit()
            return "添加成功"
        except:
            connection.rollback()
            return "添加失败"

@app.route('/user/login', methods=['POST'])
def user_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        with connection.cursor() as cursor:
            sql = "select * from login where username = '{}' and password = '{}'".format(username, password)
            result = cursor.execute(sql)
        return cursor.fetchone()
        # except:
        #     connection.rollback()
        #     return "登陆失败"

@app.route('/user/del', methods=['POST'])
def user_del():
    if request.method == "POST":
        try:
            id = int(request.form.get('id'))
            with connection.cursor() as cursor:
                sql = "delete from login where id = {}".format(int(id))
                result = cursor.execute(sql)
            connection.commit()
            if result == 0:
                return "用户不存在"
            else:
                return "删除成功"
        except:
            connection.rollback()
            return "删除失败"

@app.route('/user/update', methods=['POST'])
def user_update():
    if request.method == "POST":
        try:
            id = int(request.form.get('id'))
            password = request.form.get('password')
            with connection.cursor() as cursor:
                sql = "update login set password = '%s' where id = %d" %(password, id)
                result = cursor.execute(sql)
            connection.commit()
            return "修改成功"
        except:
            connection.rollback()
            return "修改失败"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=19090, debug=True)
    print("Good bye!")