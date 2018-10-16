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

# 获取福佳啤酒项目
def get_fujiapijiu():
    # 创建一个数据库连接
    conn = cx_Oracle.connect('survey/xunshi2018survey@10.0.1.26:1521/orcl')
    # 建立游标
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute("""select '福佳啤酒项目' as 项目名,A.allcount as 现在总完成数,B.allvisit as 总访问数,c.yestvisit as 昨天访问数,d.dvisit as 配额满,e.cvisit  as 完成,f.svisit as 甄别 from 
(select count(distinct(comuid)) as allcount from T_PROJECT t where t.pid='XS3007' and menu='C')  A,
(select count(distinct(comuid)) as allvisit from T_PROJECT t where t.pid='XS3007' and status='10')  B,
(select count(distinct(comuid)) as yestvisit from T_PROJECT t where t.pid='XS3007' and status='10' and  trunc(CREATE_TIME)=trunc(sysdate-1))  C,
(select count(distinct(comuid)) as dvisit from T_PROJECT t where t.pid='XS3007' and menu='Q') D,
(select count(distinct(comuid)) as cvisit from T_PROJECT t where t.pid='XS3007' and menu='C') E,
(select count(distinct(comuid)) as svisit from T_PROJECT t where t.pid='XS3007' and menu='S') F""")

    one = cursor.fetchone()
    return one

# 获取米凯罗啤酒数据
def get_MiKailLuo():
    # 创建一个数据库连接
    conn = cx_Oracle.connect('survey/xunshi2018survey@10.0.1.26:1521/orcl')
    # 建立游标
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute("""select '米凯罗啤酒' as 项目名,A.allcount as 现在总完成数,B.allvisit as 总访问数,c.yestvisit as 昨天访问数,d.dvisit as 配额满,e.cvisit  as 完成,f.svisit as 甄别 from 
(select count(distinct(comuid)) as allcount from T_PROJECT t where t.pid='XS3008' and menu='C')  A,
(select count(distinct(comuid)) as allvisit from T_PROJECT t where t.pid='XS3008' and status='10')  B,
(select count(distinct(comuid)) as yestvisit from T_PROJECT t where t.pid='XS3008' and status='10' and  trunc(CREATE_TIME)=trunc(sysdate-1))  C,
(select count(distinct(comuid)) as dvisit from T_PROJECT t where t.pid='XS3008' and menu='Q') D,
(select count(distinct(comuid)) as cvisit from T_PROJECT t where t.pid='XS3008' and menu='C') E,
(select count(distinct(comuid)) as svisit from T_PROJECT t where t.pid='XS3008' and menu='S') F""")

    one = cursor.fetchone()
    return one

# 获取哈尔滨啤酒控制组数据
def get_haerbincontrol():
    # 创建一个数据库连接
    conn = cx_Oracle.connect('survey/xunshi2018survey@10.0.1.26:1521/orcl')
    # 建立游标
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute("""select '哈尔滨啤酒控制组' as 项目名,A.allcount as 现在总完成数,B.allvisit as 总访问数,c.yestvisit as 昨天访问数,d.dvisit as 配额满,e.cvisit  as 完成,f.svisit as 甄别 from 
(select count(distinct(comuid)) as allcount from T_PROJECT t where t.pid='XS3003' and menu='C')  A,
(select count(distinct(comuid)) as allvisit from T_PROJECT t where t.pid='XS3003' and status='10')  B,
(select count(distinct(comuid)) as yestvisit from T_PROJECT t where t.pid='XS3003' and status='10' and  trunc(CREATE_TIME)=trunc(sysdate-1))  C,
(select count(distinct(comuid)) as dvisit from T_PROJECT t where t.pid='XS3003' and menu='Q') D,
(select count(distinct(comuid)) as cvisit from T_PROJECT t where t.pid='XS3003' and menu='C') E,
(select count(distinct(comuid)) as svisit from T_PROJECT t where t.pid='XS3003' and menu='S') F""")

    one = cursor.fetchone()
    return one

# 获取哈尔滨啤酒曝光组数据
def get_haerbinexpose():
    # 创建一个数据库连接
    conn = cx_Oracle.connect('survey/xunshi2018survey@10.0.1.26:1521/orcl')
    # 建立游标
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute("""select '哈尔滨啤酒曝光组' as 项目名,A.allcount as 现在总完成数,B.allvisit as 总访问数,c.yestvisit as 昨天访问数,d.dvisit as 配额满,e.cvisit  as 完成,f.svisit as 甄别 from 
(select count(distinct(comuid)) as allcount from T_PROJECT t where t.pid='XS3031' and menu='C')  A,
(select count(distinct(comuid)) as allvisit from T_PROJECT t where t.pid='XS3031' and status='10')  B,
(select count(distinct(comuid)) as yestvisit from T_PROJECT t where t.pid='XS3031' and status='10' and  trunc(CREATE_TIME)=trunc(sysdate-1))  C,
(select count(distinct(comuid)) as dvisit from T_PROJECT t where t.pid='XS3031' and menu='Q') D,
(select count(distinct(comuid)) as cvisit from T_PROJECT t where t.pid='XS3031' and menu='C') E,
(select count(distinct(comuid)) as svisit from T_PROJECT t where t.pid='XS3031' and menu='S') F""")

    one = cursor.fetchone()
    return one

# 获取微信接口token
def getToken(corpid,corpsecret):
    # 获取access_token
    GURL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret)
    # 使用requests.get 函数请求，并把结果转化为json形式，获取token
    token = requests.get(GURL).json()['access_token']
    return token


# 向接口发送消息
def sendMsg(title,message):
    # 获取access_token
    access_token = getToken(corpid,corpsecret)
    # 消息发送接口
    Purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"  % access_token
    # 要发送的消息
    weixin_msg = {
        "toparty": '7',      # 部门ID
        "agentid": '1000005',   # 企业应用的id
        "msgtype" : "textcard",
        "textcard": {
            "title": title,
            "description": message
        }
    }
    # 向消息接口发送消息
    print(requests.post(Purl,data = json.dumps(weixin_msg),headers={'Content-Type': 'application/json;charset=utf-8'}).content)

def send_pijiu(wenjuan_data):
    x,a,b,c,d,e,f = wenjuan_data
    title = x
    message = "截止到%s日\n总完成数：%d\n总访问数：%d\n昨日访问数：%d\n配额满：%d\n完成：%d\n甄别：%d" % ( datetime.date.today(),a,b,c,d,e,f)
    sendMsg(title,message)


if __name__ == '__main__':
    send_pijiu(get_MiKailLuo())
    send_pijiu(get_fujiapijiu())
    send_pijiu(get_haerbincontrol())
    send_pijiu(get_haerbinexpose())

