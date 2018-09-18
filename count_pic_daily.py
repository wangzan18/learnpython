import os

# 图片存储目录
path='C:\\Users\\Water\\Downloads\\vivo\\'

# 初始化变量
file = []
video = 0
jpg = 0

# 对文件夹循环
for imei in os.listdir(path):
    # 对文件夹内部日期循环
    for picdate in os.listdir(path+imei):
        # 统计某日期下面所有图片总量
        for root,dirs,files in os.walk(path+imei+"\\"+picdate):
            file += files
        # 对某个日期下面的图片和视频进行帅选，并统计数量
        for a in file:
            if os.path.splitext(a)[1] == '.mp4':
                video += 1
            else:
                jpg += 1
        # 打印文件夹名，日期名，图片数量，视频数量
        print(imei,picdate,jpg,video)
        video = 0
        jpg = 0
        file = []
