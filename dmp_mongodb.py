#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-10-16

import pymongo

# 创建连接对象以及对数据库权限认证
conn = pymongo.MongoClient("mongodb://dmp1:dmp1pass@10.0.1.26:27017/dmp")
# 选择数据库dmp
db = conn['dmp']
# 选择集合dmp_user_center
col = db['dmp_user_center']
# 获取集合中第一个文档
x = col.find_one()
print(x)
conn.close()
