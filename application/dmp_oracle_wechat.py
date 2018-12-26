#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-10-16

import json
import requests
import cx_Oracle
import datetime

# 微信公众号上应用的CropID和Secret
corpid = 'wx8d46d36104988993'
corpsecret = 'gSlRXvicrP3OP9kgZLot3CHOpchqXgN3V0KSSyqAo6s'
headers = {'Content-Type': 'application/json;charset=utf-8'}


def get_data():
    """获取数据库需要的内容

    :return: 返回查出的内容
    """
    conn = cx_Oracle.connect('gather/we2u_pcxwq58cy@10.0.1.17:1521/orcl')
    cursor = conn.cursor()

    # 查询D类安卓imei用户数
    cursor.execute("select count(distinct imei) from gather.dmp_android_imei")
    d_android_imei = cursor.fetchall()

    # 查询D类IOS用户数
    cursor.execute("select count(distinct idfa) from gather.dmp_ios_idfa")
    d_ios_idfa = cursor.fetchall()

    # 查询P类安卓imei用户数
    cursor.execute("select count(distinct CR_IMEI) from gather.dmp_user_center")
    p_android_imei = cursor.fetchall()

    # 查询D类IOS用户数
    cursor.execute("select count(distinct CR_IDFA) from gather.dmp_user_center")
    p_ios_idfa = cursor.fetchall()

    return d_android_imei[0][0], d_ios_idfa[0][0], p_android_imei[0][0], p_ios_idfa[0][0]


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
        "toparty": '8',  # 部门ID
        "agentid": '1000007',  # 企业应用的id
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


def send_dmp(data):
    """制定要给微信发送的消息

    :param data: 函数get_data，数据库查询出来的数据，是列表形式。
    """
    a, b, c, d = data
    line = '-' * 50
    title = "ComData DMP数据量统计"
    message = "截止到%s日\n" \
              "D类安卓用户：%d\n" \
              "D类IOS用户：%d\n" \
              "%s\n" \
              "P类安卓用户：%d\n" \
              "P类IOS用户：%d\n" \
              "%s" % (datetime.date.today(), a, b, line, c, d, line)
    send_wechat(title, message)


if __name__ == '__main__':
    send_dmp(get_data())
