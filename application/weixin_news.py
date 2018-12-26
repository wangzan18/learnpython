#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-09-30

import json
import requests
import sys

# 微信公众号上应用的CropID和Secret
corp_id = 'wx8d46d36104988993'
corp_secret = 'QCjzy2lH2ZB7MUG6uowChyChPsOQw96EB0X0QjofRRt0JePGezTVR4saIw3Ezznh'
headers = {'Content-Type': 'application/json;charset=utf-8'}


def get_token(corpid, corpsecret):
    """获取企业微信接口token

    :param corpid: 企业的id
    :param corpsecret: 企业应用的secret
    :return:
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret)
    # 使用requests.get 函数请求，并把结果转化为json形式，获取token
    token = requests.get(url).json()['access_token']
    return token


def send_msg(title, message):
    """向微信接口发送消息

    :param title: 消息的title
    :param message: 消息的内容
    """
    access_token = get_token(corp_id, corp_secret)
    # 消息发送接口
    purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % access_token
    # 要发送的消息
    weixin_msg = {
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
    print(requests.post(purl, data=json.dumps(weixin_msg), headers=headers).content)


if __name__ == '__main__':
    # 向脚本传参title和message
    title = sys.argv[1]
    message = sys.argv[2]
    send_msg(title, message)
