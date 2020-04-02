#!/usr/bin/python3

import pymysql as pm


def insert(sql, param):
    # 打开数据库连接
    db = pm.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="looklookdb"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    if param is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, param)

    db.autocommit(True)
    # 关闭数据库连接
    db.close()
