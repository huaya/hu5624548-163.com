# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import MySQLdb as mdb
import requests
import sys
import json

if len(sys.argv) != 3:
    raise Exception("参数错误, 需要2个参数（siteId， esCode）")

siteId=int(sys.argv[1])
esCode=str(sys.argv[2])
print("siteId: %s, esCode: %s" % (siteId, esCode))
es_codes = ['esCommonClient','esAliyuncsClient','esAliyuncs2Client','esAliyuncs3Client','esAliyuncs4Client']
if esCode not in es_codes:
    raise Exception("esCode非法, esCode: %s" % esCode)

es1_url = "http://172.20.104.35:8001/cover/site_client_map?siteId=%s&client=%s" % (siteId, esCode)
es2_url = "http://172.20.104.36:8001/cover/site_client_map?siteId=%s&client=%s" % (siteId, esCode)

es1_rs = requests.post(es1_url)
if es1_rs.status_code != 200:
    raise Exception("更改es1失败，status_code: %s" % es1_rs.status_code)
es1_re_js = json.loads(es1_rs.content.decode("UTF-8"))
res_es1_code = es1_re_js["data"][str(siteId)]
if res_es1_code != esCode:
    raise Exception("更改es1失败，res_es1_code: %s, expect_code: %s" % (res_es1_code, esCode))
print("更改es1成功")

es2_rs = requests.post(es2_url)
if es2_rs.status_code != 200:
    raise Exception("更改es2失败，status_code: %s" % es2_rs.status_code)
es2_re_js = json.loads(es2_rs.content.decode("UTF-8"))
res_es2_code = es2_re_js["data"][str(siteId)]
if res_es2_code != esCode:
    raise Exception("更改es2失败，res_es1_code: %s, expect_code: %s" % (res_es2_code, esCode))
print("更改es2成功")

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
db.autocommit(True);
cursor = db.cursor();

sql_basic = "update tb_goods_basic set update_time = DATE_ADD(update_time,INTERVAL 1 second) where `site_id` = %s" % siteId
sql_aggregation = "update tb_aggregation set update_time = DATE_ADD(update_time,INTERVAL 1 second) where `site_id` = %s" % siteId
sql_fb_pixe = "update tb_fb_pixel set update_time = DATE_ADD(update_time,INTERVAL 1 second) where `site_id` = %s" % siteId
sql_fb_pixel_rel = "update tb_fb_pixel_rel set update_time = DATE_ADD(update_time,INTERVAL 1 second) where `site_id` = %s" % siteId
sql_comment = "update tb_comment set update_time = DATE_ADD(update_time,INTERVAL 1 second) where `site_id` = %s" % siteId
sql_goods_attribute_lang = "update tb_goods_attribute_lang gal set update_time = DATE_ADD(update_time,INTERVAL 1 second) where gal.attr_id in (select ga.id from tb_goods_attribute ga where site_id = %s)" % siteId

cursor.execute(sql_basic)
cnt = cursor.rowcount
print("更新goods_basic成功, 行数：%s" % cnt)
cursor.execute(sql_aggregation)
cnt = cursor.rowcount
print("更新aggregation成功, 行数：%s" % cnt)
cursor.execute(sql_fb_pixe)
cnt = cursor.rowcount
print("更新fb_pixe成功, 行数：%s" % cnt)
cursor.execute(sql_fb_pixel_rel)
cnt = cursor.rowcount
print("更新fb_pixel_rel成功, 行数：%s" % cnt)
cursor.execute(sql_comment)
cnt = cursor.rowcount
print("更新comment成功, 行数：%s" % cnt)
cursor.execute(sql_goods_attribute_lang)
cnt = cursor.rowcount
print("更新goods_attribute_lang成功, 行数：%s" % cnt)

# 关闭数据库连接
db.close()

reload_data = {"siteId": "%s" % siteId,"esClient": "%s" % esCode}
# print(reload_data)
price_reload = "http://172.20.104.11:8001/price/reload/according/esclient"
freight_reload = "http://172.20.104.11:8001/freight/reload/according/esclient"

price_rs = requests.post(url=price_reload, json=reload_data)
if price_rs.status_code != 200:
    raise Exception("同步站点价格失败，status_code: %s" % price_rs.status_code)
print("同步站点价格成功")

freight_rs = requests.post(url=freight_reload, json=reload_data)
if freight_rs.status_code != 200:
    raise Exception("同步站点运费失败，status_code: %s" % freight_rs.status_code)
print("同步站点运费成功")
