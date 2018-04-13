# !/usr/bin/python
# coding:utf-8
import json
import urllib2
from urllib2 import URLError
import sys,argparse
import time
import requests
import datetime

__author__ = "lujin"
__version__ = "1.0.0"
__date__ = "2018-2-8"
# 批量添加 web探测监控
# 批量添加触发器

class zabbix_api:
    def __init__(self):
        self.url = 'http://*//api_jsonrpc.php' #修改URL
        self.header = {"Content-Type":"application/json"}
    def user_login(self):
        data = json.dumps({
	                       "jsonrpc": "2.0",
	                       "method": "user.login",
	                       "params": {
	                                  "user": "ansible", #修改用户名
	                                  "password": "password" #修改密码
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
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
        print response

    def trigger_create(self, hostname, name, url):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": [
                {
                    "description": name + "(%s)" %url,
                    "expression": "{%s:web.test.rspcode[%s,%s].last()}<>200" %(hostname,name,name),
                    "priority": 4
                },
                {
                    "description": name + " 3分钟无返回值" + "(%s)" %url,
                    "expression": "{%s:web.test.rspcode[%s,%s].nodata(3m)}=1" %(hostname,name,name),
                    "priority": 4
                },
            ],
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
        print response


    def get_template(self, hostname):
        data = json.dumps(
            {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": hostname
                 }
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = requests.post(self.url, data=data, headers=self.header)
        result = request.json()
        templateid = result["result"][0]["templateid"]
        return templateid


if __name__ == "__main__":
    zabbix = zabbix_api()
    # hostid = "10437"
    hostname = "test"
    hostid = zabbix.get_template(hostname)
    name_url = {}
    f = open('j.txt') #url的文件格式 名字:url
    for line in f.readlines():
        name = line.replace("：", ":").split(":", 1)[0]
        key = line.replace("：", ":").split(":", 1)[1]
        name_url[name] = key
    print name_url
    for key,value in name_url.items():
        # print key,value
        zabbix.httptest_create(hostid, key, value)
    for key, value in name_url.items():
        zabbix.trigger_create(hostname, key, value)