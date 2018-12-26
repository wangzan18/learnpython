#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

# wangzan18@126.com
# 2018-10-16

import os

# 图片存储目录
path = 'C:\\Users\\Water\\Downloads\\vivo\\'

# 初始化变量
file = []
video = 0
jpg = 0


def pic_count():
    """
    统计目录下面的图片数量，及其子目录下面的图片数量，视频数量。
    """
    for imei in os.listdir(path):

        for picdate in os.listdir(path+imei):

            for root, dirs, files in os.walk(path+imei+"\\"+picdate):
                file += files

            for a in file:
                if os.path.splitext(a)[1] == '.mp4':
                    video += 1
                else:
                    jpg += 1

            print(imei, picdate, jpg, video)
            video = 0
            jpg = 0
            file = []


pic_count()
