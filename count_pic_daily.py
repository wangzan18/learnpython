import os

# 图片存储目录
path='C:\\Users\\Water\\Downloads\\vivo\\'

file = []
video = 0
jpg = 0
for imei in os.listdir(path):
    for picdate in os.listdir(path+imei):
        for root,dirs,files in os.walk(path+imei+"\\"+picdate):
            file += files
        # print(imei,picdate,len(file))
        for a in file:
            # print(imei,picdate,a)
            if os.path.splitext(a)[1] == '.mp4':
                video += 1
            else:
                # print(imei,picdate,a)
                jpg += 1
                # print(imei,picdate,jpg)
        print(imei,picdate,jpg,video)
        video = 0
        jpg = 0
        file = []
