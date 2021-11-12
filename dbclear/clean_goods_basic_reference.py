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
sql = "select gbr.id from tb_goods_basic_reference gbr left join tb_goods_basic gb on gbr.basic_id = gb.id where gb.id is null and gbr.id >= %s and gbr.id <= %s";
delsql = "delete from tb_goods_basic_reference where id in (%s)";
while (True and statrId < endId) :
    endIdC = statrId + step;
    sql_e = sql % (statrId, endIdC)
    cursor.execute(sql_e);
    ids = cursor.fetchall();

    res = 0
    if len(ids) > 0:
        delsql_e = delsql % ("%s" % "," .join(['%d' % id for id in ids]));
        cursor.execute(delsql_e);
        res = cursor.rowcount
        cnt = cnt + res;
    print("删除数据startId: %s, endId: %s, num: %s" % (statrId, endIdC, res))

    statrId = statrId + step;
    db.autocommit(False);
    db.commit()

print("删除goods_basic_reference数据条数：%s" % cnt)
# 关闭数据库连接
db.close()

