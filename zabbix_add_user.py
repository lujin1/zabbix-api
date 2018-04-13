# coding:utf-8
import json
import requests

__author__ = "lujin"
__version__ = "2.0.0"
__date__ = "2018-4-3"
# 批量添加 web探测监控
# 批量添加触发器

class zabbix_api:
    def __init__(self):
        self.url = 'http://*//api_jsonrpc.php'  # 修改URL
        self.header = {"Content-Type": "application/json"}

    def user_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "admin",  # 修改用户名
                "password": "****"  # 修改密码
            },
            "id": 0
        })
        request = requests.post(self.url, data=data, headers=self.header)
        result = request.json()
        authID = result["result"]
        return authID

    def get_usergroup(self, usergroup):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "usergroup.get",
                "params": {
                    "output": "extend",
                    "filter": {
                        "name": usergroup
                    }
            },
            "auth": self.user_login(),
            "id": 1
        }
        )
        request = requests.post(self.url, data=data, headers=self.header)
        result = request.json()
        # print result["result"][0]["name"]
        usrgrpid = result["result"][0]["usrgrpid"]
        return usrgrpid

    def user_create(self, usrgrpid, alias, name, passwd, email, sms):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.create",
                "params": {
                    "alias": alias,
                    "name": name,
                    "passwd": passwd,
                    "usrgrps": [
                        {
                            "usrgrpid": usrgrpid
                        }
                    ],
                    "user_medias": [
                        {
                            "mediatypeid": "1",
                            "sendto": email,
                            "active": 0,
                            "severity": 63,
                            "period": "1-7,00:00-24:00"
                        },
                        {
                            "mediatypeid": "3",
                            "sendto": sms,
                            "active": 0,
                            "severity": 63,
                            "period": "1-7,00:00-24:00"
                        }
                    ]
                },
                "auth": self.user_login(),
                "id": 1
        })
        request = requests.post(self.url, data=data, headers=self.header)
        re = request.json()
        try:
            userid = re["result"]
            return "添加成功，用户id为：\n %s" %(userid)
        except:
            return "添加失败，详情为：\n %s" %(re)
if __name__ == "__main__":
    zabbix = zabbix_api()
    usrgrpid = zabbix.get_usergroup("亳州")
    zabbix.user_create(usrgrpid, alias, name, passwd, email, sms)