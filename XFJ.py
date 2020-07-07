from locust import HttpLocust,TaskSet,task,between,HttpUser,events
import queue,re,requests
import random,time,json
from Common import Secret,readData,Common,SSO
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Performance_Testing(TaskSet):

    @task()
    def loginbyphone(self):
        a=int(time.time()*1000)
        b=random.randint(0,10000000000)
        phone=readData.ReadData().phone()
        print("登录的手机号为：",phone)
        dict={
            "version":"4.0",
            "timestamp":str(a),
            "program-params":"devid,siteid,phone",
            "devid":"429A9EC0-58DE-41D6-B79A-4E073350FA38",
            "token":"",
            "random":str(b),
            "phone":str(phone),
            "siteid":"1"
        }
        secret_url="devid="+dict["devid"]+"&random="+dict["random"]+"&timestamp="+dict["timestamp"]\
               +"&token="+dict["token"]+"&version="+dict["version"]
        secret=Secret.md5(secret_url)
        program_sign_url="devid="+dict["devid"]+"&siteid="+dict["siteid"]+"&phone="+dict["phone"]+"&secret="+secret
        program_sign=Secret.md5(program_sign_url)
        headers={
            "version":dict["version"],
            "timestamp":dict["timestamp"],
            "program-params":dict["program-params"],
            "devid":dict["devid"],
            "token":dict["token"],
            "program-sign":program_sign,
            "random":dict["random"]
        }
        body={
            "phone":dict["phone"],
            "devid":dict["devid"],
            "siteid":dict["siteid"]
        }
        self.client.headers.update(headers)
        req=self.client.post(":18443/sso-app/api/loginByPhone",body,verify=False,name="账号登录")
        js=json.loads(req.content)
        if js["msg"]=="success":
            print("账号登录成功")
            print(js)
        else:
            print("登录失败")
            print(js)

    @task()
    def get_Articles(self):
        i=random.randint(10,1220)
        colid=Common.common().article_columns()
        print("当前窗口的栏目为：",colid)
        params={
            "siteId":"1",
            "columnId":str(colid),
            "curVersions":"1"
        }
        req=self.client.get("/app_if/getArticles",params=params,verify=False,name="查看稿件列表")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("获取栏目数据成功")
            print(js)
        else:
            print("获取栏目数据失败")
            print(js)

    @task()
    def article_content1(self):
        aid=Common.common().article_lists(5)
        params={
            "siteId":"1",
            "articleId":str(aid),
            "curVersions":"1"
        }
        req=self.client.get("/app_if/getArticleContent",params=params,verify=False,name="查看图文稿件详情")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("查看稿件详情成功")
            print(js)
        else:
            print("查看稿件失败")
            print(js)

    @task()
    def article_content2(self):
        aid=Common.common().article_lists(15)
        params={
            "siteId":"1",
            "articleId":str(aid),
            "curVersions":"1"
        }
        req=self.client.get("/app_if/getArticleContent",params=params,verify=False,name="查看视频稿件详情")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("查看稿件详情成功")
            print(js)
        else:
            print("查看稿件失败")
            print(js)

    @task()
    def article_content3(self):
        aid=Common.common().article_lists(16)
        params={
            "siteId":"1",
            "articleId":str(aid),
            "curVersions":"1"
        }
        req=self.client.get("/app_if/getArticleContent",params=params,verify=False,name="查看直播稿件详情")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("查看稿件详情成功")
            print(js)
        else:
            print("查看稿件失败")
            print(js)

    @task()
    def article_content4(self):
        aid=Common.common().article_lists(242)
        params={
            "siteId":"1",
            "articleId":str(aid),
            "curVersions":"1"
        }
        req=self.client.get("/app_if/getArticleContent",params=params,verify=False,name="查看链接稿件详情")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("查看稿件详情成功")
            print(js)
        else:
            print("查看稿件失败")
            print(js)

    @task()
    def article_share(self):
        id=Common.common().article_lists(5)
        params={
            "id":str(id),
            "type":"0",
            "eventType":"2",
            "channel":"2",
            "siteID":"1",
            "curVersions":"1"
        }
        req=self.client.get("/app_if/event",params=params,verify=False,name="稿件分享")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("稿件分享成功")
            print(js)
        else:
            print("稿件分享失败")

    @task()
    def article_vote(self):
        phone=readData.ReadData().account()
        print("参与投票的用户手机号为：",phone)
        userid=SSO.loginbyphone(phone)
        devid=int(time.time()*1000)
        headers={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        body={
            "siteID":"1",
            "userID":userid,
            "username":"12345",
            "userOtherID":str(devid),
            "voteID":"173",
            "voteResult":"172:244"
        }
        self.client.headers.update(headers)
        req=self.client.post("/app_if/vote",body,verify=False,name="稿内投票")
        js=json.loads(req.content)
        if js["result"]=="true":
            print("投票成功")
            print(js)
        else:
            print("投票失败")
            print(js)

    @task()
    def activity_list(self):
        params={
            "catID":"-1",
            "siteID":"1",
            "curVersions":"1"
        }
        req=self.client.get("/app_if/activityList",params=params,verify=False,name="查看活动列表数据")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("获取活动列表数据成功")
            print(js)
        else:
            print("获取活动列表数据失败")
            print(js)

    @task()
    def activity_detail(self):
        fid=Common.common().activity_list()
        params={
            "fileId":fid,
            "siteID":"1",
            "curVersions":"1"
        }
        req=self.client.get("/app_if/activityDetail",params=params,verify=False,name="查看活动详情数据成功")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("查看活动详情数据成功")
            print(js)
        else:
            print("查看活动详情数据失败")
            print(js)

    @task()
    def activity_save(self):
        headers={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        phone=readData.ReadData().account()  #此处用新账号：1、避免重复报名；2、增大并发量
        userid=SSO.loginbyphone(phone)
        t=int(time.time()*1000)
        print("当前报名的用户手机号为：",phone)
        fid=Common.common().activity_list()   #避免性能测试期间无法验证活动功能，此处不适用动态值
        signForm="{"+"entry_phone:"+str(phone)+","+"entry_realName:"+"老张"+"}"
        body={
            "fileId":"470",
            "userID":userid,
            "siteId":"1",
            "device":str(t),
            "phone":str(phone),
            "signForm":signForm,
            "imgUrl":"",
            "curVersions":"1"
        }
        self.client.headers.update(headers)
        req=self.client.post("/app_if/saveActivity",body,verify=False,name="活动报名")
        js=json.loads(req.content)
        if js["message"]=="报名成功":
            print("活动报名成功")
            print(js)
        else:
            print("活动报名存在异常")
            print(js)

    @task()
    def fjh_xyRank(self):
        phone=readData.ReadData().account()
        userid=SSO.loginbyphone(phone)
        params={
            "siteID":"1",
            "type":"0",
            "userID":userid,
            "device":"1234567890-dasd",
            "curVersions":"1"
        }
        req=self.client.get("/app_if/xyRank",params=params,verify=False,name="查看影响力榜单")
        js=json.loads(req.content)
        if js["message"]=="操作成功":
            print("获取影响力榜单数据成功")
            print(js)
        else:
            print("获取榜单数据失败")
            print(js)

    @task()
    def fjh_topicSub(self):
        headers={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        phone=readData.ReadData().phone()  #此处用新账号：1、避免重复报名；2、增大并发量
        userid=SSO.loginbyphone(phone)
        devid=int(time.time()*1000)
        print("当前打榜的用户手机号为：",phone)
        body={
            "siteID":"1",
            "type":"4",
            "id":"98",
            "userID":userid,
            "device":str(devid),
            "curVersions":"1"
        }
        self.client.headers.update(headers)
        req=self.client.post("/app_if/topicSub",body,verify=False,name="福建号订阅")
        js=json.loads(req.content)
        if js["message"]=="success":
            print("福建号订阅成功")
            print(js)
        else:
            print("订阅失败")
            print(js)

    @task()
    def fjh_hitXyBulletin(self):
        headers={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        phone=readData.ReadData().phone()  #此处用新账号：1、避免重复报名；2、增大并发量
        userid=SSO.loginbyphone(phone)
        print("当前打榜的用户手机号为：",phone)
        devid=int(time.time()*1000)
        body={
            "siteID":"1",
            "id":"98",
            "userID":userid,
            "device":str(devid),
            "curVersions":"1"
        }
        self.client.headers.update(headers)
        req=self.client.post("/app_if/hitXyBulletin",body,verify=False,name="福建号打榜")
        js=json.loads(req.content)
        if js["message"]=="操作成功":
            print("福建号打榜成功")
            print(js)
        else:
            print("打榜失败")
            print(js)



class MyUser(HttpUser):
    tasks=[Performance_Testing]
    wait_time=between(1,30)
    host='https://api1.fjdaily.com'

if __name__ == "__main__":
    import os
    os.system("locust -f XFJ.py")