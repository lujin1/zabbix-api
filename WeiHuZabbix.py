# !/usr/bin/python
# coding:utf-8
# by lujin
# zabbix 添加删除维护状态
# 入参 内网ip + （1|0）
# 1 == 添加主机维护
# 0 == 删除主机维护
# 维护时间为30分钟
# 2017-12-05
import json
import urllib2
from urllib2 import URLError
import sys,argparse
import time
import datetime

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
    def host_get(self,hostName=''):
        data=json.dumps({
	            "jsonrpc": "2.0",
	            "method": "host.get",
	            "params": {
	                      "output": "extend",
	                      "filter":{"host":hostName}
	                      },
	            "auth": self.user_login(),
	            "id": 1
	            })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
         #   print ("主机数量: %s"%(len(response['result'])))
            for host in response['result']:
                status = {"0":"OK","1":"Disabled"}
             #   available = {"0":"Unknown","1":"available","2":"Unavailable"}
            if len(hostName)==0:
                print ("HostID: %s HostName: %s"%(host['hostid'],host['name']))
            else:
                print ("HostID: %s HostName: %s"%(host['hostid'],host['name']))
                return host['hostid'], host["maintenance_status"]
        except UnboundLocalError:
            print '主机监控不存在！'

    def maintenance_get(self):
        data = json.dumps({
                "jsonrpc": "2.0",
                "method": "maintenance.get",
                "params": {
                        "hostids": "10204",
                 },
                 "auth": self.user_login(),
                 "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            print response
            try:
                maintenanceid = response['result'][0]['maintenanceid']
                result.close()
                return maintenanceid
            except:
                print "该主机未添加维护！"

    def maintenance_create(self,hostip,host):
        dtime = datetime.datetime.now()
        btime = dtime + datetime.timedelta(hours=0.5)
        ans_dtime = time.mktime(dtime.timetuple())
        ans_btime = time.mktime(btime.timetuple())
        data = json.dumps({
                "jsonrpc": "2.0",
                "method": "maintenance.create",
                "params": {
                     "name": hostip,
                     "active_since": ans_dtime,
                     "active_till": ans_btime,
                     "hostids": [
                        host
                     ],
                    "timeperiods": [
                        {
                            "timeperiod_type": 0,
                            "every": 1,
                            "dayofweek": 64,
                            "start_time": 64800,
                            "period": 1800
                        }
                 ]
                },
                "auth": self.user_login(),
                "id": 1
        })
        request = urllib2.Request(self.url, data)
        try:
            for key in self.header:
                request.add_header(key, self.header[key])
                result = urllib2.urlopen(request)
                response = json.loads(result.read())
                #print response
                result.close()
                print "创建维护成功！"
        except:
            print "创建维护失败！"

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
    hostip = sys.argv[1]
    action = sys.argv[2]
    host = zabbix.host_get(hostip)[0]
    if host is not None:
        if action == '1':
            maintenanceid = zabbix.maintenance_get()
            if maintenanceid is None:
                zabbix.maintenance_create(hostip, host)
                while 1:
                    maintenance_status = zabbix.host_get(hostip)[1]
                    print maintenance_status
                    if maintenance_status == "1":
                        break
            else:
                print "创建失败，已存在该主机的维护 主机：%s" %(hostip)
        elif action == '0':
            maintenanceid = zabbix.maintenance_get()
            print maintenanceid
            if maintenanceid is not None:
                zabbix.maintenance_delete(maintenanceid)
                while 1:
                    maintenance_status = zabbix.host_get(hostip)[1]
                    print maintenance_status
                    if maintenance_status == "0":
                        break
                print "删除成功！"
            else:
                print "删除失败，该主机不存在维护状态 主机：%s" %(hostip)
    else:
        print "exit......."
        sys.exit()