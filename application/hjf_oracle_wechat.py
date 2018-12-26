#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-09-30

import json
import requests
import cx_Oracle
import datetime

# 微信公众号上应用的CropID和Secret
corp_id = 'wx8d46d36104988993'
corp_secret = 'QCjzy2lH2ZB7MUG6uowChyChPsOQw96EB0X0QjofRRt0JePGezTVR4saIw3Ezznh'
headers = {'Content-Type': 'application/json;charset=utf-8'}

def hjf_zhuce():
    """查询数据库
    查询oracle数据库，并把查询的结果返回
    :return:
    """

    conn = cx_Oracle.connect('test/password@10.0.2.64:1521/unicode')

    cursor = conn.cursor()

    cursor.execute("""select A.allCount 总注册人数,B.yesterDayRegCount 昨天注册的人数,C.yesterDaySignCount 昨天登录的人数 from 
    (select count(1) as allCount from m_user where trunc(registerDate) >=to_date('2018-01-01','yyyy-MM-dd')) A,
    (select count(1) as yesterDayRegCount from m_user where trunc(registerDate)=trunc(sysdate-1)) B ,
   ( select count(1) as yesterDaySignCount from m_usersign where trunc(signtime)=trunc(sysdate-1)) C""")

    one = cursor.fetchone()
    cursor.close()
    conn.close()
    return one


def get_token(corpid, corpsecret):
    """获取微信接口token

    :param corpid: 企业id
    :param corpsecret: 应用密码串
    :return: 返回获取到的token
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret)
    # 使用requests.get 函数请求，并把结果转化为json形式，获取token
    token = requests.get(url).json()['access_token']
    return token


def send_msg(title, message):
    """向微信接口发送消息
    向微信发送textcard格式的消息
    :param title: 消息的title
    :param message: 消息的内容
    """
    access_token = get_token(corp_id, corp_secret)
    # 消息发送接口
    purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % access_token
    # 要发送的消息
    wechat_msg = {
        "toparty": '2',  # 部门ID
        "agentid": '4',  # 企业应用的id
        "msgtype": "textcard",
        "textcard": {
            "title": title,
            "description": message,
            "url": "www.wzlinux.com",
            "btntxt": "更多"
        }
    }
    # 向消息接口发送消息
    print(requests.post(purl, data=json.dumps(wechat_msg), headers=headers).content)


if __name__ == '__main__':
    x, y, z = hjf_zhuce()
    a = "惠积分用户信息通知"
    b = "截止到%s日\n惠积分总注册用户：%d人\n昨日新增人数：%d人\n昨日签到人数：%d人\n【创数科技】" % ( datetime.date.today(), x, y, z)
    send_msg(a, b)

