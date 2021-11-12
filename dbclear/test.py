# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import MySQLdb as mdb
import sys

if len(sys.argv) != 4:
    raise Exception("参数错误, 需要三个参数（statrId， endId， step）")

statrId=int(sys.argv[1])
endId=int(sys.argv[2])
step=int(sys.argv[3])
print("startId: %s, endId: %s, step: %s" % (statrId, endId, step))

cf = cp.ConfigParser()
cf.read("./db.config")

# 打开数据库连接
db = mdb.connect(
    host=cf.get("db", "host"),
    port=cf.getint("db", "port"),
    user=cf.get("db", "user"),
    passwd=cf.get("db", "passwd"),
    database=cf.get("db", "database")
)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor();

cnt = 0;
sql = "select now() from dual";
cursor.execute(sql);
now = cursor.fetchone();
print("now: %s" % now[0])
# 关闭数据库连接
db.close()

