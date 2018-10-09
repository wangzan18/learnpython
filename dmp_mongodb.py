# -*- coding: UTF-8 -*-
# wangzan18@126.com

import pymongo

myclient = pymongo.MongoClient("mongodb://dmp:dmp@10.0.1.26:27017/dmp")
mydb = myclient["dmp"]
mycol = mydb["dmp"]
print(mycol)