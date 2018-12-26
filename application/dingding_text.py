#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

# wangzan18@126.com
# 2018-09-30

import requests
import json
import sys

headers = {'Content-Type': 'application/json;charset=utf-8'}

# 获取群机器人接口
api_url = "https://oapi.dingtalk.com/robot/send?access_token=" \
          "787ff7bd0e71074e297bd7853fad956a6dc3ef5a82150548acd1c0b9de13fb26"


def msg(title, text):
    """
    向钉钉接口发送消息
    :param title: 消息的名称
    :param text:  消息的内容
    """
    json_text= {
     "msgtype": "link",
     "link": {
            "title": title,
            "text": text,
            "messageUrl": "http://www.wzlinux.cn"
        },
     "at": {
            "atMobiles": [
                "18817511111"
            ],
            "isAtAll": False
        }
    }

    print(requests.post(api_url, json.dumps(json_text), headers=headers).content)


if __name__ == '__main__':
    a = sys.argv[1]
    b = sys.argv[2]
    msg(a, b)
