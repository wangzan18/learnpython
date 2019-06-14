#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-09-30

import requests
import pymysql
import json
import datetime

# 微信公众号上应用的CropID和Secret
corpid = 'wwb6fffa8f234dd513'
corpsecret = 'xAQHWhqt92NuoVAsQra6-bDuT2rIWAAYo1ghjMGfRDU'
headers = {'Content-Type': 'application/json;charset=utf-8'}


def get_data():
    """ 连接数据，获取数据

    :return: 返回查询的数据
    """
    conn = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='wzlinux18',
        db='tecno',
        charset='utf8'
    )
    cursor = conn.cursor()
    cursor.execute("select count(1) from tecno.tc_user_info;")
    all_data = cursor.fetchone()
    cursor.execute("SELECT count(1) FROM tecno.tc_user_info WHERE TO_DAYS(NOW()) - TO_DAYS(rec_update_time) = 1;")
    yes_data = cursor.fetchone()
    conn.close()
    return all_data[0], yes_data[0]


def get_token(corp_id, corp_secret):
    """获取微信接口token
    :param corp_id: 企业的id
    :param corp_secret: 应用的secret
    :return: 返回获取到的token
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corp_id, corp_secret)
    # 使用requests.get 函数请求，并把结果转化为json形式，获取token
    token = requests.get(url).json()['access_token']
    return token


def send_wechat(title, message):
    """向接口发送消息函数
    :param title: 消息的标题
    :param message: 消息的内容
    """
    access_token = get_token(corpid, corpsecret)

    purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % access_token

    wechat_msg = {
        "toparty": '2',  # 部门ID
        "agentid": '1000002',  # 企业应用的id
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


def send_msg(data):
    """制定要给微信发送的消息
    :param data: 函数get_data，数据库查询出来的数据，是列表形式。
    """
    a, b = data
    title = "TECNO非洲活动数据统计"
    message = "截止到%s日\n" \
              "总激活用户：%d\n" \
              "昨日激活用户：%d\n" % (datetime.date.today(), a, b)
    send_wechat(title, message)


if __name__ == '__main__':
    send_msg(get_data())
