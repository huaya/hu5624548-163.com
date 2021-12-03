# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import MySQLdb as mdb
import sys

if len(sys.argv) != 3:
    raise Exception("参数错误, 需要2个参数（aggregation_id, delNum）")

aggregation_id=int(sys.argv[1])
delNum=int(sys.argv[2])
print("aggregation_id: %s" % (aggregation_id))

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

cnt = 0
sql = '''select 
            a.id 
        from tb_aggregation_item a 
        where a.aggregation_id  = %s 
        and a.id not in (
            select t.maxid from (
                select b.basic_id, b.tab_id,  max(b.id) as maxid from tb_aggregation_item b 
                where b.aggregation_id  = %s and yn = '1'
                GROUP BY b.basic_id, b.tab_id
                ) t
        )'''
sql_e = sql % (aggregation_id, aggregation_id)

delsql = "delete from tb_aggregation_item where id = %s"

cursor.execute(sql_e);
ids = cursor.fetchall();
cnt = 0

for id in ids:
    delsql_e = delsql % id
    cursor.execute(delsql_e);

    print("删除数据aggregation_item, id: %s" % id)
    db.autocommit(True)
    cnt = cnt + 1
    if cnt >= delNum:
        break

print("删除aggregation_item数据条数：%s" % cnt)
# 关闭数据库连接
db.close()

