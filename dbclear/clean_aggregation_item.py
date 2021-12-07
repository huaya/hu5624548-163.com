# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import MySQLdb as mdb
import sys

if len(sys.argv) != 3:
    raise Exception("参数错误, 需要2个参数（statrId， endId）")

statrId=int(sys.argv[1])
endId=int(sys.argv[2])
print("startId: %s, endId: %s" % (statrId, endId))

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


sql = "select DISTINCT ai.basic_id from tb_aggregation_item ai left join tb_goods_basic gb on ai.basic_id = gb.id where gb.id is null and ai.id >= %s and ai.id <= %s;"
delsql = "delete from tb_aggregation_item where basic_id = %s"

sql_e = sql % (statrId, endId)
cursor.execute(sql_e);
ids = cursor.fetchall();

cnt = 0
if len(ids) > 0:
    for id in ids:
        delsql_e = delsql % id
        cursor.execute(delsql_e);
        res = cursor.rowcount
        cnt = cnt + res;
        print("删除数据aggregation_item, basic_id: %s, num: %s" % (id, res))
        db.autocommit(True);

print("删除aggregation_item数据条数：%s, basicId个数：%s" % (cnt, len(ids)))
# 关闭数据库连接
db.close()

