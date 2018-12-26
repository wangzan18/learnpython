#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-09-30

import requests
import pymysql
import json

headers = {'Content-Type': 'application/json;charset=utf-8'}

# 建立数据库连接
conn = pymysql.Connect(
    host='10.0.1.18',
    port=3306,
    user='root',
    passwd='password',
    db='tmall_basic',
    charset='utf8'
)

# 获取群机器人接口
api_url = "https://oapi.dingtalk.com/robot/send?access_token=" \
          "787ff7bd0e71074e297bd7853fad956a6dc3ef5a82150548acd1c0b9de13fb26"


def msg(text):
    """向钉钉接口发送消息

    :param text: 消息内容格式
    """
    json_text = {
     "msgtype": "text",
     "text": {
            "content": text
        },
     "at": {
            "atMobiles": [
                "18817511223"
            ],
            "isAtAll": False
        }
    }
    # 向接口发送数据，并返回处理结果
    print(requests.post(api_url, json.dumps(json_text), headers=headers).content)


cursor = conn.cursor()

 
# 1、从数据库中查询
sql = "SHOW TABLES"
# cursor执行sql语句
cursor.execute(sql)
# 打印执行结果的条数
print(cursor.rowcount)

# 将所有的结果放入rr中
rr = cursor.fetchall()

# 对每个表进行循环
for table in rr:
    # 查询每个表的结构
    sql1 = "DESC %s" % table
    cursor.execute(sql1)
    rr1 = cursor.fetchall()
    msg(rr1)

   
# 数据库连接和游标的关闭
cursor.close()
conn.close()
