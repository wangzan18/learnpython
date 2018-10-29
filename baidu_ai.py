#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-10-19

import requests
import base64
import urllib
import os
import os.path

api_key = "SsZE4DPhmFISxcAEGU3SNM0y"
secret_key = "8gYUc3aCkBFce70NlEvmOfSVkTLZH3fm"
path = 'C:\\Users\\Water\\Downloads\\123\\'
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


def file_path():
    """获取目录下所有文件路径，返回一个列表

    """
    file_name = os.listdir(path)
    file = []
    for i in file_name:
        file.append(path + i)
    return file


def get_pic_data():
    """请求接口图片数据

    """
    access_token = get_token(api_key, secret_key)
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token
    a = open('C:\\Users\\Water\\Downloads\\baidu_api.csv', 'a+')
    for jpg in file_path():
        f = open(jpg, 'rb')
        # 参数image：图像base64编码
        img = base64.b64encode(f.read())
        params = {"image": img}
        params = urllib.parse.urlencode(params)
        response_data = requests.post(url, data=params).json()
        a.write(os.path.basename(jpg) + ',')
        for word in response_data['words_result']:
            # print(word['words'], end=',')
            a.write(word['words'] + ',')
        a.write('\n')
        f.close()
    a.close()


if __name__ == '__main__':
    get_pic_data()


