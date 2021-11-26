# coding=UTF-8
#!/usr/bin/python3
import configparser as cp
import redis

cf = cp.ConfigParser()
cf.read("./db.config")

rd = redis.StrictRedis(host=cf.get("redis", "host"), port=cf.getint("redis", "port"), password=cf.get("redis", "password"),db=cf.getint("redis", "database"), decode_responses=True)

ids=[43437,43438]

rd.zrem("cloud-update-queue:goods:wait1", *tuple(ids))

rd.close()

