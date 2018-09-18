#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os

headers = {'Content-Type': 'application/json;charset=utf-8'}

api_url = "https://oapi.dingtalk.com/robot/send?access_token=19f597062cfbbfc9de27fd5c80667e18eef094e6cbc5ab8552ec05de731d2c17"

def msg(text):

    json_text= {
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

    print requests.post(api_url,json.dumps(json_text),headers=headers).content

if __name__ == '__main__':
    text = sys.argv[1]
    msg(text)
