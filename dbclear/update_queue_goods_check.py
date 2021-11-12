# coding=UTF-8
#!/usr/bin/python3

import configparser as cp
import MySQLdb as mdb
import redis
import sys

if len(sys.argv) != 4:
    raise Exception("参数错误, 需要三个参数（statrId， endId， step）")

statrId=int(sys.argv[1])
endId=int(sys.argv[2])
step=int(sys.argv[3])

#解析配置文件
cf = cp.ConfigParser()
cf.read("./db.config")

# 打开数据库连接
db = mdb.connect(host=cf.get("db", "host"),port=cf.getint("db", "port"),user=cf.get("db", "user"),passwd=cf.get("db", "passwd"),database=cf.get("db", "database"))
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor();
sql = "select count(id) from tb_goods_basic where id = %s";

rd = redis.StrictRedis(host=cf.get("redis", "host"), port=cf.getint("redis", "port"), password=cf.get("redis", "password"),db=cf.getint("redis", "database"), decode_responses=True)
queue_key = "cloud-update-queue:goods:wait";

while (True and statrId < endId) :
    endIdC = statrId + step;
    goods = rd.zrange(queue_key, statrId, endIdC);
    for g in goods:
        cursor.execute(sql % g)
        cnt = cursor.fetchone();
        if cnt[0] == 0:
            res = rd.zrem(queue_key, g);
            print("移除商品：%s, 结果：%s" % (g, res))

    statrId = statrId + step;

rd.close()
db.close()