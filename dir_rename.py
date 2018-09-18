import os

# 图片存储目录
path='C:\\Users\\Water\\Downloads\\vivo\\'

# 打开列表
f = open(path+"file.csv","r")
f1= open(path+'lost.txt','w')
# 读取文件第一行
line = f.readline()
while line:
    # 切换到照片目录
    os.chdir(path)
    # 截取列表里面的字段以及要更换的字段
    i,j=line.split(",")[0],line.split(",")[1].replace('\n','')
    # print(i,j)
    # 判断，如果不存在的文件夹，可以跳过并记录导出到lost.txt.
    if os.path.exists(i):
        os.rename(i,j)
    else:
        f1.write(i+","+j+"\n")
    line = f.readline()
# 关闭文件
f.close()
f1.close()
