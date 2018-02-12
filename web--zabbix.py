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
__date__ = "2018-2-8"
# 批量添加 web探测监控
# 批量添加触发器

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
	                                  "password": "***@123" #修改密码
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
    def httptest_create(self, hostid, name, url):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "httptest.create",
                "params": {
                    "name": name,
                    "hostid": hostid,
                    "steps": [
                        {
                            "name": name,
                            "url": url,
                            "status_codes": 200,
                            "no": 1
                        },
                    ]
                },
                "auth": self.user_login(),
                "id": 1
            }
        )
        request = urllib2.Request(self.url, data)
        print request
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            print response

    def trigger_create(self, name, url):
        data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": [
                {
                    "description": name + "(%s)" %url,
                    "expression": "{web for yunke:web.test.rspcode[%s,%s].last()}<>200" %(name,name),
                    "priority": 4
                },
                {
                    "description": name + " 3分钟无返回值" + "(%s)" %url,
                    "expression": "{web for yunke:web.test.rspcode[%s,%s].nodata(3m)}=1" %(name,name),
                    "priority": 4
                },
            ],
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        print request
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            print response




if __name__ == "__main__":
    zabbix = zabbix_api()
    # hostid = "10279"
    # name = "云科-认证平台"
    # url = "http://117.161.11.38:8090"
    name_url = {
        "云科-认证平台": "http://117.161.11.38:8090",
        "云科-接口": "http://117.161.11.38:9000/auth_inter/his/inhospital/queryPrefeeMaster.next?INPATIENT_NO=11&HOSPITAL_MARK=11",
        "云科-his": "http://117.161.11.38:9001/his",
        "云科-pacs": "http://117.161.11.38:8080",
        "云科-hcrm": "117.161.11.38:8081/cloud"
    }
    # hostid = "10281"
    # name_url = {
    #     "闻康-认证平台1": "http://39.106.134.248",
    #     "闻康-认证平台2": "http://39.106.131.226",
    #     "闻康-HIS-1": "http://47.93.198.168/login.htm",
    #     "闻康-HIS-2": "http://39.106.134.171/login.htm",
    #     "闻康-接口": "http://59.110.145.248/auth_inter/his/inhospital/queryPrefeeMaster.next?INPATIENT_NO=11&HOSPITAL_MARK=11",
    #     "闻康-pacs1": "http://39.106.134.230/main/login.jsp",
    #     "闻康-pacs2": "http://39.106.134.242/main/login.jsp"
    # }

    # print type(name_url)
    # for key,value in name_url.items():
    #     print key,value
    #     print zabbix.httptest_create(hostid, key, value)
    # print zabbix.trigger_create()
    # for key in name_url:
    #     print zabbix.trigger_create(key)
    for key, value in name_url.items():
        print zabbix.trigger_create(key,value)
