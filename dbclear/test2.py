# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import redis
import requests
import json
import sys

siteId=int(sys.argv[1])
esCode=str(sys.argv[2])
price_reload = "http://res.beta.orderplus.com/price/reload/according/esclient"
reload_data = {"siteId": "%s" % str(siteId),"esClient": "%s" % esCode}

price_rs = requests.post(url=price_reload, json=reload_data)
if price_rs.status_code != 200:
    raise Exception("登录失败，status_code: %s" % price_rs.status_code)
js_res = json.loads(price_rs.content.decode("UTF-8"))
print(js_res)