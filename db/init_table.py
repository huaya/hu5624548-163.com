#!/usr/bin/python3

import pymysql as pm


sql = "INSERT INTO `tb_goods_attribute_rel` (`yn`, `create_uid`, `create_time`, `update_uid`, `update_time`, `goods_id`, `attr_val_id`) VALUES %s"

value = "(1, 0, '2018-11-14 10:20:56', 0, '2018-11-14 10:20:56', 880673, 5137)"

# 打开数据库连接
db = pm.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="orderplus-db"
)
list = []
for num in range(1, 1000) :
    list.append(value)
av = "%s" % "," .join(['%s' % v for v in list])
sql_ex = sql % av

for i in range(1, 100000) :
    cursor = db.cursor()
    cursor.execute(sql_ex)
    db.autocommit(True)
    print("插入成功 %s" % i)

# 关闭数据库连接
db.close()