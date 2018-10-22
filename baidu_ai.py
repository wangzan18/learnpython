#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-10-19

import requests
import base64
import urllib

api_key = "SsZE4DPhmFISxcAEGU3SNM0y"
secret_key = "8gYUc3aCkBFce70NlEvmOfSVkTLZH3fm"
pic = "C:\\Users\\Water\\Downloads\\ele.jpg"
headers = {'Content-Type', 'application/x-www-form-urlencoded'}


def get_token(ak, sk):
    """获取百度AI接口token

    :param ak: 百度云应用的AK
    :param sk: 百度云应用的SK
    :return: 返回我们需要的token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"\
          % (ak, sk)
    token = requests.get(url).json()['access_token']
    return token


def get_pic_data():
    """请求接口图片数据

    """
    access_token = get_token(api_key, secret_key)
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
    # 二进制方式打开图文件
    f = open(pic, 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    params = urllib.parse.urlencode(params)
    response_data = requests.post(url, data=params).json()
    for word in response_data['words_result'][2:]:
        print(word['words'], end=',')
    f.close()


get_pic_data()




