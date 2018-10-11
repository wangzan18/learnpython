#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

# wangzan18@126.com
# 2018-09-30

import requests
import json
import sys

headers = {'Content-Type': 'application/json;charset=utf-8'}

# 获取群机器人接口
api_url = "https://oapi.dingtalk.com/robot/send?access_token=787ff7bd0e71074e297bd7853fad956a6dc3ef5a82150548acd1c0b9de13fb26"


def msg(title,text):
    # 接口消息类型，具体可以查看官方接口文档
    json_text= {
     "msgtype": "link",
        "link": {
            "title" : title,
            "text": text,
            "messageUrl" : "http://www.huijifen.cn"
        },
        "at": {
            "atMobiles": [
                "18817511223"
            ],
            "isAtAll": False
        }
    }
    # 向接口发送数据，并返回处理结果
    print(requests.post(api_url,json.dumps(json_text),headers=headers).content)

if __name__ == '__main__':
    title = sys.argv[1]   # 获取传递的第一个参数
    text = sys.argv[2]
    msg(title,text)
