#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import requests
import time
import threading
from concurrent import futures

connect = {
    "host": "10.0.1.18",
    "port": 3306,
    "user": "root",
    "passwd": "xunshi2015",
    "db": "test_db",
    "charset": "utf8"
}
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

conn = pymysql.connect(**connect)
cur = conn.cursor()

result = []
total = 1
lock = threading.Lock()


def run(url):
    req = requests.get(url, headers=headers, timeout=6).json()
    time.sleep(0.5)
    try:
        data = req['data']
        if data['view'] != "--" and data['aid'] != 0:
            video = (
                data['aid'],  # 视频编号
                data['view'],  # 播放量
                data['danmaku'],  # 弹幕数
                data['reply'],  # 评论数
                data['favorite'],  # 收藏数
                data['coin'],  # 硬币数
                data['share'],  # 分享数
                ""  # 视频名称（暂时为空）
            )
            with lock:
                result.append(video)
    except Exception as e:
        print("请求错误为 %s" % e)


def create_db():
    global cur
    cur.execute("""create table if not exists bili_video
                           (v_aid int primary key,
                            v_view int,
                            v_danmaku int,
                            v_reply int,
                            v_favorite int,
                            v_coin int,
                            v_share int,
                            v_name text)""")


def save_db():
    global result, cur, conn
    sql = "insert into bili_video values(%s, %s, %s, %s, %s, %s, %s, %s);"
    for row in result:
        try:
            cur.execute(sql, row)
        except Exception as e:
            print(e)
            conn.rollback()
    conn.commit()
    result = []


if __name__ == '__main__':
    create_db()
    print("启动爬虫，开始爬取数据")
    for i in range(4000, 5000):
        begin = 1000 * i
        urls = ["https://api.bilibili.com/x/web-interface/archive/stat?aid={}".format(j)
                for j in range(begin, begin + 1000)]
        with futures.ThreadPoolExecutor(64) as executor:
            executor.map(run, urls)
        save_db()
        print("插入第%s -- %s数据" % (begin, begin + 1000))
    print("爬虫结束")
    conn.close()
