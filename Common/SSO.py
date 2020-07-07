#coding=utf-8

import requests,re,os
from Common import Secret,readData
import json,random,time
from requests_toolbelt import MultipartEncoder

# host='https://appif.allcitysz.com'
host='https://api1.fjdaily.com:18443'
"""注册"""
def register(phone,psw):
    url=host+"/sso-app/api/register"
    a=int(time.time()*1000)
    b=random.randint(0,10000000000)
    dict={
        "version":"4.0",
        "timestamp":str(a),
        "devid":"3FAC4E73-9345-4515-92FA-59616B1B218C",
        "token":"",
        "random":str(b),
        "program-params":"password,phone",
        "password":Secret.md5(psw),
        "phone":str(phone)
    }
    sercet_url="devid="+dict["devid"]+"&random="+dict["random"]+\
               "&timestamp="+dict["timestamp"]+"&token="+dict["token"]+"&version="+dict["version"]
    md5_secret=Secret.md5(sercet_url)
    program_sign_url="password="+dict["password"]+"&phone="+dict["phone"]+"&secret="+md5_secret
    program_sign=Secret.md5(program_sign_url)
    headers={
        "devid":dict["devid"],
        "random":str(b),
        "timestamp":str(a),
        "token":"",
        "version":"4.0",
        "program-sign":program_sign,
        "Content-Type":"application/x-www-form-urlencoded",
        "program-params":"password,phone"
    }
    body={
        "password":dict["password"],
        "phone":dict["phone"],
        "siteid":"4"
    }
    s=requests.session()
    s.headers.update(headers)
    req=s.post(url,data=body)
    js=json.loads(req.content)
    return js

"""登录"""
def login(phone,psw):
    url=host+":8082/sso-app/api/login"
    a=int(time.time()*1000)
    b=random.randint(0,10000000000)
    dict={
            "devid":"3FAC4E73-9345-4515-92FA-59616B1B218C",
            "random":str(b),
            "timestamp":str(a),
            "token":"",
            "version":"4.0",
            "password":Secret.md5(psw),
            "phone":phone
        }
    secret_url="devid="+dict["devid"]+"&random="+dict["random"]+"&timestamp="+\
                   dict["timestamp"]+"&token="+dict["token"]+"&version="+dict["version"]
    md5_secret=Secret.md5(secret_url)
    progarm_sign_url="devid="+dict["devid"]+"&password="+dict["password"]+\
                         "&phone="+dict["phone"]+"&secret="+md5_secret
    progarm_sign=Secret.md5(progarm_sign_url)
    headers={
            "devid":dict["devid"],
            "random":str(b),
            "timestamp":str(a),
            "token":"",
            "version":"4.0",
            "program-sign":progarm_sign,
            "Content-Type":"application/x-www-form-urlencoded",
            "program-params":"devid,password,phone"
        }
    body={
            "devid":dict["devid"],
            "password":dict["password"],
            "phone":dict["phone"]
        }
    s=requests.session()
    s.headers.update(headers)
    req=s.post(url,data=body)
    js=json.loads(req.content)
    return js

"""忘记密码"""
def forgetPassword(phone,psw):
    url=host+'/sso-app/api/forgetPassword'
    a=int(time.time()*1000)
    b=int(random.randint(0,10000000000)*0.1)
    dict={
        "timestamp":str(a),
        "devid":"429A9EC0-58DE-41D6-B79A-4E073350FA38",
        "token":"",
        "random":str(b),
        "version":"4.0",
        "phone":phone,
        "password":Secret.md5(psw)
    }
    secret_url="devid="+dict["devid"]+"&random="+dict["random"]+"&timestamp="+dict["timestamp"]+\
               "&token="+dict["token"]+"&version="+dict["version"]
    md5_secret=Secret.md5(secret_url)
    progarm_sign_url="phone="+dict["phone"]+"&password="+dict["password"]+"&secret="+md5_secret
    progarm_sign=Secret.md5(progarm_sign_url)
    headers={
        "devid":dict["devid"],
        "version":"4.0",
        "timestamp":dict["timestamp"],
        "program-params":"phone,password",
        "token":"",
        "program-sign":progarm_sign,
        "random":dict["random"]
    }
    body={
        "phone":dict["phone"],
        "password":dict["password"]
    }
    s=requests.session()
    s.headers.update(headers)
    req=s.post(url,data=body)
    js=json.loads(req.content)
    return js

"""退出登录"""
def logout(phone,psw):
    req=login(phone,psw)
    url=host+'/sso-app/api/logout'
    a=int(time.time()*1000)
    b=random.randint(0,10000000000)
    dict={
            "devid":"3FAC4E73-9345-4515-92FA-59616B1B218C",
            "random":str(b),
            "timestamp":str(a),
            "token":req['value']['token'],
            "version":"4.0",
            "uid":req['value']['uid']
        }
    secret_url="devid="+dict["devid"]+"&random="+dict["random"]+"&timestamp="+\
                   dict["timestamp"]+"&token="+dict["token"]+"&version="+dict["version"]
    md5_secret=Secret.md5(secret_url)
    progarm_sign_url="devid="+dict["devid"]+"&token="+dict["token"]+\
                         "&uid="+dict["uid"]+"&secret="+md5_secret
    progarm_sign=Secret.md5(progarm_sign_url)
    headers={
            "devid":dict["devid"],
            "random":str(b),
            "timestamp":str(a),
            "token":dict["token"],
            "version":"4.0",
            "program-sign":progarm_sign,
            "Content-Type":"application/x-www-form-urlencoded",
            "program-params":"devid,token,uid",
            "Accept-Language":"zh-cn"
        }
    body={
            "devid":dict["devid"],
            "token":dict["token"],
            "uid":req['value']['uid']
        }
    s=requests.session()
    s.headers.update(headers)
    req=s.post(url,data=body)
    js=json.loads(req.content)
    return js

"""变更绑定手机号"""
def changephone(phone,psw,newphone):
    url=host+'/sso-app/api/changePhone'
    a=int(time.time()*1000)
    b=random.randint(0,10000000000)
    s=login(phone,psw)
    token=s['value']["token"]
    uid=s['value']["uid"]
    dict={
        "version":"4.0",
        "timestamp":str(a),
        "program-params":"uid,newPhone",
        "devid":"429A9EC0-58DE-41D6-B79A-4E073350FA38",
        "token":token,
        "random":str(b),
        "uid":uid,
        "newPhone":newphone
    }
    secret_url="devid="+dict["devid"]+"&random="+dict["random"]+"&timestamp="+dict["timestamp"]+\
               "&token="+dict["token"]+"&version="+dict["version"]
    secret=Secret.md5(secret_url)
    program_sign_url="uid="+dict["uid"]+"&newPhone="+dict["newPhone"]+"&secret="+secret
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
        "uid":dict["uid"],
        "newPhone":dict["newPhone"],
        "siteid":"4"
    }
    s=requests.session()
    s.headers.update(headers)
    req=s.post(url,data=body)
    js=json.loads(req.content)
    return js

"""上传账号头像"""
def uploadPortrait(phone,psw):
    result=login(phone,psw)
    url='https://app.gzdaily.cn:4443/app_if/amuc/api/member/uploadPortrait'
    a=random.randint(0,10000000000)
    b=int(time.time()*1000)
    dict={
        "devid":"429A9EC0-58DE-41D6-B79A-4E073350FA38",
        "version":"4.0",
        "timestamp":str(b),
        "program-params":"uid",
        "token":result["value"]["token"],
        "random":str(a),
        "uid":result["value"]["userid"]
    }
    secret_url="devid="+dict["devid"]+"&random="+dict["random"]+"&timestamp="+dict["timestamp"]\
               +"&token="+dict["token"]+"&version="+dict["version"]
    secret=Secret.md5(secret_url)
    program_sign_url="uid="+dict["uid"]+"&secret="+secret
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
    file_payload={"data":("image.jpg",open("D:\\10.jpg","rb"),"application/octet-stream")}
    m=MultipartEncoder(file_payload)
    headers["Content-Type"]=m.content_type
    new_url=url+"?uid="+dict["uid"]
    s=requests.session()
    s.headers.update(headers)
    req=s.post(new_url,data=m)
    print(req)
    js=json.loads(req.content)
    return js

"""变更用户信息"""
def modify(phone,psw,nickname="GZ",sex="1",birthday="2000-01-01"):
    url=host+"/sso-app/api/modify"
    result=login(phone,psw)
    a=int(time.time()*1000)
    b=random.randint(0,10000000000)
    dict={
        "version":"4.0",
        "timestamp":str(a),
        "program-params":"uid,nickname,sex,birthday",
        "devid":"429A9EC0-58DE-41D6-B79A-4E073350FA38",
        "token":result["value"]["token"],
        "uid":result["value"]["uid"],
        "nickname":nickname,
        "sex":sex,
        "birthday":birthday,
        "random":str(b)
    }
    secret_url="devid="+dict["devid"]+"&random="+dict["random"]+"&timestamp="+dict["timestamp"]\
               +"&token="+dict["token"]+"&version="+dict["version"]
    secret=Secret.md5(secret_url)
    program_sign_url="uid="+dict["uid"]+"&nickname="+dict["nickname"]+"&sex="\
                     +dict["sex"]+"&birthday="+dict["birthday"]+"&secret="+secret
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
    s=requests.session()
    s.headers.update(headers)
    body={
        "uid":dict["uid"],
        "nickname":dict["nickname"],
        "sex":dict["sex"],
        "birthday":dict["birthday"]
    }
    req=s.post(url,data=body)
    js=json.loads(req.content)
    return js

def loginbyphone(phone):
    url=host+'/sso-app/api/loginByPhone'
    a=int(time.time()*1000)
    b=random.randint(0,10000000000)
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
    s=requests.session()
    s.headers.update(headers)
    req=s.post(url,data=body)
    js=json.loads(req.content)
    # print(type(js["value"]["userid"]))
    return js["value"]["userid"]

# phone='13545390158'
# psw='test123'
# s=login(phone,psw)
# print(s)
# print(type(s))
# print(s["value"]["userid"])
# phone=13545390012
# phone=readData.ReadData().account()
# print(loginbyphone(phone))
# print(type(loginbyphone(phone)))

