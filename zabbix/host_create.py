#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-12-26

import requests
import json

# 初始化参数
zabbix_api = "http://zabbix.comratings.com/api_jsonrpc.php"
headers = {'Content-Type': 'application/json'}
username = 'admin'
password = 'xunshi2012'


# 登录zabbix并获取auth的token
def get_toekn():
    login = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": ""+username+"",
            "password": ""+password+""
        },
        "id": 1,
        "auth": None
    }
    auth = requests.post(zabbix_api, data=json.dumps(login), headers=headers)
    return auth.json()["result"]


token = get_toekn()

# 检索主机

host_get = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": [
            "hostid",
            "host"
        ],
        "selectInterfaces": [
            "interfaceid",
            "ip"
        ]
    },
    "id": 2,
    "auth": ""+token+""
}
hostid_get = requests.post(zabbix_api, data=json.dumps(host_get), headers=headers)
hostid_get = hostid_get.json()
for i in hostid_get['result']:
    print(i["host"])
