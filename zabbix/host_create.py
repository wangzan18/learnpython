#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-12-26

import requests

zabbix_api = "http://zabbix.comratings.com/api_jsonrpc.php"
headers = {'Content-Type', 'application/json-rpc'}


def get_api_version():
    data = {"jsonrpc": "2.0", "method": "apiinfo.version", "id": 1, "auth": null, "params": {}}
    r = requests.post(zabbix_api, data=data, headers=headers)
    print(r.text)


get_api_version()