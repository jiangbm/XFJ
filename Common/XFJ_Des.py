#coding=utf-8

import base64,binascii,pyDes,re,hashlib,time
from Crypto.Cipher import DES3
from urllib import request

def des(apiData,appKey,appSecret):
    #切片提取密钥
    api_data=apiData[38:42]+apiData[2:16]+apiData[31:33]+apiData[21:25]
    #将appkey和appsecret进行base64解码(并转成str类型) //文档中未注明
    bkey=str(base64.b64decode(appKey),encoding='utf-8')
    bsecret=str(base64.b64decode(appSecret),encoding='utf-8')

    # 将解码后的16进制字节转成字节数组(即bytes和bytearray之间的转换) //此处文档备注省略了，需将16进制字节转为2进制
    # akey=bytearray(bkey)
    # asecret=bytearray(bsecret)
    akey=bytes.fromhex(bkey)
    asecret=bytes.fromhex(bsecret)
    # 通过密钥对字节数组进行3des解密
    """方法一"""
    key=DES3.new(api_data,DES3.MODE_ECB)
    truek=key.decrypt(akey)
    #因为解密后的长度默认为24位，会默认填充/x08补位，此处需通过正则过滤
    truekey=re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('',truek.decode())

    trues=key.decrypt(asecret)
    truesecret=re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('',trues.decode())
    return truekey,truesecret


    # """方法二"""
    # k=pyDes.triple_des(api_data,pyDes.ECB,"\0\0\0\0\0\0\0\0",pad=None, padmode=pyDes.PAD_NORMAL)
    # e=k.decrypt(akey,padmode=pyDes.PAD_NORMAL)
    # print(e)
    #
    # """方法三"""
    # de_appkey=base64.standard_b64decode(appKey)
    # # pkey=key.decrypt(de_appkey)

def md5(str):
     m=hashlib.md5()
     m.update(str.encode("utf8"))
     return m.hexdigest()
# apiData='MTU5MDc0OTE1NjU2NDE1OTA3NDkxNTY1NjQxNTkwNzQ5MTU2NTY0'
# appKey='OTQzYzFkOTE2MGVlMjExNGNkMmVjY2M2YmNmOGU4NmQ3NDM3MGU4ODZmYmU3MGEwZDkxNmI3MWVlMzk0OThlMGJmZjg5YmIxZGQ4M2I3NzM='
# appSecret='MmM2NmQ2OGEwZTc5MjAyYWNiMDlhYzJjNjYwOTRhNjFjNGU1YzRkNGQ4ZWNhOWJjODNmYTA4ZWZjMTFhMzg3ZWJmZjg5YmIxZGQ4M2I3NzM='
# l=list(des(apiData,appKey,appSecret))
# print(l)
# t=int(time.time()*1000)
# print(t)
# s=l[1]+str(t)+l[1][3:7]
# print(md5(s))

def des_token(apiData,authtoken):
    #切片提取密钥
    api_data=apiData[40:45]+apiData[5:21]+apiData[33:36]
    #将token进行base64解码(并转成str类型)
    token=str(base64.b64decode(authtoken),encoding='utf-8')
    #将16进制字符串转为二进制
    atoken=bytes.fromhex(token)
    #通过提取的密钥对二进制数组token进行解密
    key=DES3.new(api_data,DES3.MODE_ECB)
    truet=key.decrypt(atoken)
    #因为解密后的长度默认为24位，会默认填充/x08补位，此处需通过正则过滤
    truetoken=re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('',truet.decode())
    return truetoken