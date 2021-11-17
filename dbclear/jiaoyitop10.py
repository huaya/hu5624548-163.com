# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import MySQLdb as mdb
import numpy
import matplotlib
from matplotlib import pyplot as plt
from pandas import *

#读取数据库配置文件
cf = cp.ConfigParser()
cf.read("./db-pro-rd.config")

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

top10sql = '''
select
s.name as '站名',
yd.yestaday_sum as '昨总量',
IFNULL(td.today_sum, 0) as '今天累计',
IFNULL(ydn.yd_now_sum, 0) as '昨同时间'
from (select
x.site_id,
sum(x.t_sum) as yestaday_sum
from (
				SELECT
						if(b.parent_id = 0, b.site_id, b.parent_site_id) as site_id,
						count(*) as t_sum
				FROM tb_order a
				inner join tb_site b on a.site_id = b.site_id and b.yn ='1'
				where a.status >= '3' and a.special_sign='0'
				and a.create_time  >= CONCAT(date_format(date_sub(now(), interval 1 day),'%y-%m-%d'), ' 00:00:00')
				and a.create_time  <= CONCAT(date_format(date_sub(now(), interval 1 day),'%y-%m-%d'), ' 23:59:59')
				GROUP BY b.site_id
) x
GROUP BY x.site_id
ORDER BY t_sum DESC 
LIMIT 10 ) yd
inner join tb_site s on s.site_id = yd.site_id
left join (
		select
				y.site_id,
				sum(y.t_sum) as today_sum
	from (
			SELECT
				if(b.parent_id = 0, b.site_id, b.parent_site_id) as site_id,
				count(*) as t_sum
			FROM tb_order a
			inner join tb_site b on a.site_id = b.site_id and b.yn ='1'
			where a.status >= '3' and a.special_sign='0'
			and a.create_time >= CONCAT(DATE_FORMAT(now(),'%Y-%m-%d'), ' 00:00:00')
			and a.create_time <= now()
			GROUP BY b.site_id
		) y
		GROUP BY y.site_id
) td on yd.site_id = td.site_id
left join (
		select
				z.site_id,
				sum(z.t_sum) as yd_now_sum
		from (
			SELECT
				if(b.parent_id = 0, b.site_id, b.parent_site_id) as site_id,
				count(*) as t_sum
			FROM tb_order a
			inner join tb_site b on a.site_id = b.site_id and b.yn ='1'
			where a.status >= '3' and a.special_sign='0'
			and a.create_time >= CONCAT(date_format(date_sub(now(), interval 1 day),'%y-%m-%d'), ' 00:00:00')
			and a.create_time <= date_sub(now(), interval 1 day)
			GROUP BY b.site_id
		) z
		GROUP BY z.site_id
) ydn on ydn.site_id = td.site_id''';

count = cursor.execute(top10sql.encode("UTF-8"))
if count:
    result = cursor.fetchall()
    aaa = numpy.array(result, str)

    matplotlib.rcParams['font.family']='SimHei'
    idx = Index(numpy.arange(1,11))

    df = DataFrame(aaa, index=idx, columns=['站名', '昨总量', '今天累计', '昨同时间'])

    fig = plt.figure(figsize=(8,3))
    ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[])

    the_table=plt.table(cellText=aaa, colLabels=df.columns, colWidths=[0.2] * aaa.shape[1], loc='center',cellLoc='center')
    the_table.set_fontsize(20)
    the_table.scale(1.2,1.3)

    plt.show()
else:
    print("无数据")

db.close()

