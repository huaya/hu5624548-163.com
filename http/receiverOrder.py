import requests
import json

url = "http://gateway.orderplus.com/frontend-machine/platformOrderInfo/receiverOrder"
with open("./data/site_order.csv") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if i == 0: continue;
        line = line.strip()
        site_id, order_no, status = line.split(",")
        data = {"SiteId": site_id, "OrderNo": order_no}
        r = requests.post(url=url, data=json.dumps(data))
        if (r.status_code != 200):
            print("推送失败, status_code:{} site_id:{} order_no:{}".format(r.status_code, site_id, order_no))
            continue
        res = json.loads(r.text)
        if res["code"] != 200:
            print("推送失败, status_code:{} site_id:{} order_no:{}".format(r.status_code, site_id, order_no))
            continue
        print("推送成功, status_code:{} code:{} timestamp:{}".format(r.status_code, res["code"], res["timestamp"]))