#coding=utf-8
import requests,json,base64,time,pyDes
from Common import XFJ_Des

host='https://api1.fjdaily.com'
def authinfo():
    t=int(time.time()*1000)
    params={
        "t":str(t),
        "siteId":"1",
        "siteID":"1"
    }
    s=requests.session()
    url=host+"/app_if/authinfo"
    #不允许接口重定向
    req=s.get(url,params=params,allow_redirects=False)
    js=json.loads(req.content)
    key=js["data"]["appKey"]
    secret=js["data"]["appSecret"]
    #获取headers中的参数
    api_data=req.headers["api-data"]
    l=XFJ_Des.des(api_data,key,secret)
    return list(l)

def auth():
    t=int(time.time()*1000)
    key=authinfo()[0]
    secret=authinfo()[1]
    sign_url=secret+str(t)+secret[2:7]
    sign=XFJ_Des.md5(sign_url)
    headers={
        "Content-Type":"application/x-www-form-urlencoded"
    }
    body={
        "appKey":key,
        "time":str(t),
        "sign":sign,
        "t":str(t),
        "siteId":"1",
        "siteID":"1"
    }
    url=host+'/app_if/auth'
    s=requests.session()
    s.headers.update(headers)
    req=s.post(url,data=body,allow_redirects=False)
    js=json.loads(req.content)
    authtoken=js["data"]["authToken"]
    apiData=req.headers["api-data"]
    s=XFJ_Des.des_token(apiData,authtoken)
    return s

def sign():
    t=int(time.time()*1000)
    secret=authinfo()[1]
    token=auth()
    sign_url=token+secret+str(t)
    s=XFJ_Des.md5(sign_url)
    print(t)
    print(token)
    print(s)
    return s,t

print(sign())




