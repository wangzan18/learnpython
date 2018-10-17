#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-09-30

import json
import requests
import cx_Oracle
import datetime

# 微信公众号上应用的CropID和Secret
corpid = 'wx8d46d36104988993'
corpsecret = 'QCjzy2lH2ZB7MUG6uowChyChPsOQw96EB0X0QjofRRt0JePGezTVR4saIw3Ezznh'

# 获取数据库数据
def hjf_zhuce():
    # 创建一个数据库连接
    conn = cx_Oracle.connect('test/comratings@10.0.2.64:1521/unicode')
    # 建立游标
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute("""select A.allCount 总注册人数,B.yesterDayRegCount 昨天注册的人数,C.yesterDaySignCount 昨天登录的人数 from 
    (select count(1) as allCount from m_user where trunc(registerDate) >=to_date('2018-01-01','yyyy-MM-dd')) A,
    (select count(1) as yesterDayRegCount from m_user where trunc(registerDate)=trunc(sysdate-1)) B ,
   ( select count(1) as yesterDaySignCount from m_usersign where trunc(signtime)=trunc(sysdate-1)) C""")

    one = cursor.fetchone()
    conn.close()
    cursor.close()
    return one

# 获取微信接口token
def getToken(corpid,corpsecret):
    # 获取access_token
    GURL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret)
    # 使用requests.get 函数请求，并把结果转化为json形式，获取token
    token = requests.get(GURL).json()['access_token']
    return token


# 向接口发送消息
def sendMsg(title,message):
    # 获取access_token
    access_token = getToken(corpid,corpsecret)
    # 消息发送接口
    Purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"  % access_token
    # 要发送的消息
    weixin_msg = {
        "toparty": '2',      # 部门ID
        "agentid": '4',   # 企业应用的id
        "msgtype" : "textcard",
        "textcard": {
            "title": title,
            "description": message,
            "url": "www.wzlinux.com",
            "btntxt": "更多"
        }
    }
    # 向消息接口发送消息
    print(requests.post(Purl,data = json.dumps(weixin_msg),headers={'Content-Type': 'application/json;charset=utf-8'}).content)

if __name__ == '__main__':
    # 向脚本传参title和message
    x,y,z = hjf_zhuce()
    title = "惠积分用户信息通知"
    message = "截止到%s日\n惠积分总注册用户：%d人\n昨日新增人数：%d人\n昨日签到人数：%d人\n【创数科技】" % ( datetime.date.today(),x,y,z)
    sendMsg(title,message)
