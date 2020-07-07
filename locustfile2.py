#coding:utf-8

import random,time,json
from locust import HttpUser,TaskSet,User,task,between
from Common import Secret
# from requests_toolbelt import MultipartEncoder
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# sys.path.append(os.getcwd())

class MyUser(TaskSet):
    a = int(time.time() * 1000)
    b = random.randint(0, 10000000000)
    dict = {
        "provider": "apple",
        "oid": "001587",
        "nickname": "APPLE001587",
        "devid": "123456",
        "siteid": "1",
        "random": str(b),
        "timestamp": str(a),
        "version": "1.0.0",
        "token": "1",
        "curVersions": "1"
    }
    secret_url = "devid=" + dict["devid"] + "&random=" + dict["random"] + "&timestamp=" + dict["timestamp"] \
                + "&token=" + dict["token"] + "&version=" + dict["version"]
    md5_secret = Secret.md5(secret_url)
    @task(1)
    def OauthLogin(self):
        body = {
            "provider": "apple",
            "oid": "001587",
            "nickname": "APPLE001587",
            "devid": "123456",
            "siteid": "1",
            "random": str(self.b),
            "timestamp": str(self.a),
            "version": "1.0.0",
            "token": "1",
            "curVersions": "1"
        }
        program_sign_url = "devid=" + body["devid"] + "&random=" + body["random"] + "&timestamp=" + body["timestamp"] \
                           + "&token=" + body["token"] + "&version=" + body["version"] + "&secret=" + self.md5_secret
        program_sign = Secret.md5(program_sign_url)
        headers = {
            "devid": self.dict["devid"],
            "random": str(self.b),
            "timestamp": str(self.a),
            "token": "1",
            "version": self.dict["version"],
            "program-sign": program_sign,
            "Content-Type": "application/x-www-form-urlencoded",
            "program-params": "devid,random,timestamp,token,version"
        }
        self.client.headers.update(headers)
        r = self.client.post('/api/oauthLogin',body,verify=False,name="第三方账号登录")
        if r.content:
            response_data = json.loads(r.content)
            print("三方登录")
            print(response_data)
            assert response_data['code'] == 1

    @task(1)
    def Logout(self):
        body = {
            "uid": "174",
            "token": "1",
            "devid": "123456"
        }
        program_sign_url2 = "uid=" + body["uid"] + "&devid=" + body["devid"] + "&token=" + body[
            "token"] + "&secret=" + self.md5_secret
        program_sign2 = Secret.md5(program_sign_url2)
        headers2 = {
            "devid": body["devid"],
            "random": str(self.b),
            "timestamp": str(self.a),
            "token": "1",
            "version": self.dict["version"],
            "program-sign": program_sign2,
            "Content-Type": "application/x-www-form-urlencoded",
            "program-params": "uid,devid,token"
        }
        self.client.headers.update(headers2)
        r = self.client.post('/api/logout',body,verify=False,name="账号退出")
        if r.content:
            response_data = json.loads(r.content)
            print("退出账号")
            print(response_data)
            assert response_data['code'] == 0

class MyUser(HttpUser):
    tasks = [MyUser]
    host = 'https://api1.fjdaily.com:18443/sso-app'
    wait_time = between(3,6)

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile2.py")