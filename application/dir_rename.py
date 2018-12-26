#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-10-16

import os

# 图片存储目录
path = 'C:\\Users\\Water\\Downloads\\vivo\\'


f = open(path+"file.csv", "r")
f1 = open(path+'lost.txt', 'w')

line = f.readline()

# 循环查找，修改目录名称
while line:

    os.chdir(path)

    i, j = line.split(",")[0], line.split(",")[1].replace('\n', '')

    if os.path.exists(i):
        os.rename(i, j)
    else:
        f1.write(i+"," + j + "\n")
    line = f.readline()

# 关闭文件
f.close()
f1.close()
