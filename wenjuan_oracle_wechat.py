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
corpsecret = 'fm2SOjoOGI8HrOb2n3S1r4OE9G5R52I1aGWFnVpTd-E'
headers = {'Content-Type': 'application/json;charset=utf-8'}
# 各项目组编号
fujia = 'XS3007'
mikailuo = 'XS3008'
haerbin_control = 'XS3003'
haerbin_expose = 'XS3031'


def get_data(project_id):
    """获取数据库需要的内容

    :param project_id: 需要传入的项目id，在程序开始又定义
    :return: 返回查出的内容
    """
    try:
        conn = cx_Oracle.connect('survey/xunshi2018survey@10.0.1.26:1521/orcl')
    except UnboundLocalError:
        print("无法连接数据库")

    cursor = conn.cursor()

    cursor.execute("""select menu, count(distinct(comuid))
  from T_PROJECT t
 where t.pid = '%s'
 group by menu
 order by menu""" % project_id)

    one = cursor.fetchall()
    dict_one = dict(one)

    cursor.execute(""" select count(distinct(comuid))
  from T_PROJECT t
 where t.pid = '%s' and menu = 'C'
   and trunc(CREATE_TIME) = trunc(sysdate - 1)""" % project_id)

    two = cursor.fetchall()

    cursor.execute(""" select count(distinct(comuid))
      from T_PROJECT t
     where t.pid = '%s' and status = '10'
       and trunc(CREATE_TIME) = trunc(sysdate - 1)""" % project_id)

    three = cursor.fetchall()

    cursor.close()
    conn.close()
    return dict_one, two, three


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


def send_msg(title, message):
    """向接口发送消息函数

    :param title: 消息的标题
    :param message: 消息的内容
    """
    access_token = get_token(corpid, corpsecret)

    purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % access_token

    wechat_msg = {
        "toparty": '2',  # 部门ID
        "agentid": '1000005',  # 企业应用的id
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


def send_wenjuan(x, all, data):
    """制定要给微信发送的消息

    :param x: 为消息的标题内容，即项目内容
    :param all: 当前项目目标数，向相关人员获取
    :param data: 函数get_data，数据库查询出来的数据，是列表形式。
    """
    a, b, c = data
    title = x
    message = "截止到%s日\n" \
              "总目标数：%d\n" \
              "总完成数：%d\n" \
              "差额：%d\n" \
              "总配额满：%d\n" \
              "总甄别数：%d\n" \
              "昨日完成：%d\n" \
              "昨日访问：%d" % (datetime.date.today(), all, a['C'], all - a['C'], a['Q'], a['S'], b[0][0], c[0][0])
    send_msg(title, message)


if __name__ == '__main__':
    send_wenjuan('米凯罗啤酒', 250, get_data(mikailuo))
    send_wenjuan('福佳啤酒', 1000, get_data(fujia))
    send_wenjuan('哈尔滨啤酒控制组', 200, get_data(haerbin_control))
    send_wenjuan('哈尔滨啤酒曝光组', 200, get_data(haerbin_expose))
