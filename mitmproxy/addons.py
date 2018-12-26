#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-12-14

from mitmproxy import http


class ModifyHost:
    @staticmethod
    def request(flow: http.HTTPFlow):
        if flow.request.pretty_host == "baidu.com":
            flow.request.host = "www.so.com"
        elif flow.request.path.endswith("/brew"):
            flow.response = http.HTTPResponse.make(418, "I am a teapot", )


add = ModifyHost()
