# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import MySQLdb as mdb
import sys

if len(sys.argv) != 2:
    raise Exception("参数错误, 需要2个参数（pokayoke）")

pokayoke=sys.argv[1]
print("pokayoke: %s" % (pokayoke))
if pokayoke != "清理":
    raise Exception("防错参数错误, pokayoke: %s" % pokayoke)

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
db.autocommit(False)

data_sql = '''select
                        ai.aggregation_id,
                        ai.basic_id,
                        ai.tab_id,
                        count(*) as cnt
                from tb_aggregation_item ai
                where ai.yn = '1' 
                GROUP BY ai.aggregation_id, ai.tab_id, ai.basic_id
                HAVING count(*) > 1
                order by cnt desc'''

sql = '''select 
                a.id 
        from tb_aggregation_item a 
        where a.yn= '1' and a.aggregation_id  = %s and a.basic_id = %s and a.tab_id = %s
        and a.id != (
                select max(b.id) as maxid from tb_aggregation_item b 
                where b.yn = '1' and b.aggregation_id  = a.aggregation_id and b.basic_id = a.basic_id and b.tab_id = a.tab_id
        )'''
del_sql = "delete from tb_aggregation_item where id in (%s)"

cursor.execute(data_sql);
datas = cursor.fetchall()
total = 0
for data in datas:
    aggregation_id = data[0]
    basic_id = data[1]
    tab_id = data[2]
    cnt = data[3]
    sql_e = sql % (aggregation_id, basic_id, tab_id)

    cursor.execute(sql_e)
    ids = cursor.fetchall()
    if len(ids) != cnt -1:
        print("汇总id数不等于明细ID数， 汇总数: %s， 明细数：%s " % (cnt -1, len(ids)))
        continue

    del_sql_e = del_sql % ("%s" % ','.join(["%d" % id for id in ids]))
    cursor.execute(del_sql_e)
    resnum = cursor.rowcount
    if resnum != len(ids):
        print("删除id数不等于明细ID数， 删除数: %s， 明细数：%s " % (resnum, len(ids)))
        db.rollback()
    else:
        total = total + cnt - 1
        db.commit()
        print("删除成功， 删除数: %s " % resnum)

print("删除aggregation_item数据条数：%s" % total)
# 关闭数据库连接
db.close()

