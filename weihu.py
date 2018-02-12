# !/usr/bin/python
# coding:utf-8
import json
import urllib2
from urllib2 import URLError
import sys,argparse
import time
import datetime

__author__ = "lujin"
__version__ = "1.0.0"
__date__ = "2018-2-12"
# 删除过期的维护

class zabbix_api:
    def __init__(self):
        self.url = 'http://***/api_jsonrpc.php' #修改URL
        self.header = {"Content-Type":"application/json"}
    def user_login(self):
        data = json.dumps({
	                       "jsonrpc": "2.0",
	                       "method": "user.login",
	                       "params": {
	                                  "user": "***", #修改用户名
	                                  "password": "***123" #修改密码
	                                  },
	                       "id": 0
	                       })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print 'url error for zabbix ', e
            sys.exit()
        try:
            response = json.loads(result.read())
            result.close()
            self.authID = response['result']
            return self.authID
        except KeyError:
            print 'user or password error!'
            sys.exit()

    def maintenance_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "maintenance.get",
                "params": {},
                "auth": self.user_login(),
                "id": 1
            }
        )
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            # print response
            return response['result']

    def maintenance_delete(self,maintenanceid):
        data = json.dumps({
                "jsonrpc": "2.0",
                "method": "maintenance.delete",
                "params": [
                    maintenanceid
                ],
                "auth": self.user_login(),
                "id": 1
            })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            #print response
            result.close()

if __name__ == "__main__":
    zabbix = zabbix_api()
    result = zabbix.maintenance_get()
    n = len(result)
    now_time = time.time()
    # print now_time
    for i in range(n):
        active_till = result[i]['active_till']
        if int(active_till) < int(now_time):
            maintenanceid = result[i]['maintenanceid']
            zabbix.maintenance_delete(maintenanceid)
            name = result[i]['name']
            print u"已删除过期的维护: %s" %name
        else:
            print "没有过期的维护"