import pymysql

 
# 建立数据库连接
conn = pymysql.Connect(
    host='10.0.1.18',
    port=3306,
    user='root',
    passwd='xunshi2015',
    db='tmall_basic',
    charset='utf8'
)
 
# 使用cursor()方法创建一个游标对象 cursor
cursor = conn.cursor()

 
# 1、从数据库中查询
sql = "SHOW TABLES"
# cursor执行sql语句
cursor.execute(sql)
# 打印执行结果的条数
print(cursor.rowcount)

# 将所有的结果放入rr中
rr = cursor.fetchall()

# 对每个表进行循环
for table in rr:
    # 查询每个表的结构
    sql1 = "DESC %s" % table
    cursor.execute(sql1)
    rr1 = cursor.fetchall()
    print("\n")
    print(table)
    # 打印每一个字段
    for field in rr1:
        print(field)


# 数据库连接和游标的关闭
conn.close()
cursor.close()
