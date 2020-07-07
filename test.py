#coding=utf-8

import base64,binascii,pyDes
from Crypto.Cipher import DES3

apiData=' MTU5MDc0OTE1NjU2NDE1OTA3NDkxNTY1NjQxNTkwNzQ5MTU2NTY0'
#切片提取密钥
api_data=apiData[38:42]+apiData[2:16]+apiData[31:33]+apiData[21:25]
print(api_data)
appKey='OTQzYzFkOTE2MGVlMjExNGNkMmVjY2M2YmNmOGU4NmQ3NDM3MGU4ODZmYmU3MGEwZDkxNmI3MWVlMzk0OThlMGJmZjg5YmIxZGQ4M2I3NzM='
appSecret='MmM2NmQ2OGEwZTc5MjAyYWNiMDlhYzJjNjYwOTRhNjFjNGU1YzRkNGQ4ZWNhOWJjODNmYTA4ZWZjMTFhMzg3ZWJmZjg5YmIxZGQ4M2I3NzM='
#将appkey和appsecret进行base64解码
bkey=base64.b64decode(appKey)
bsecret=base64.b64decode(appSecret)

# 将解码后的16进制字节转成字节数组(即bytes和bytearray之间的转换)
akey=bytearray(bkey)
asecret=bytearray(bsecret)

# 通过密钥对字节数组进行3des解密
"""方法一"""
key=DES3.new(api_data,DES3.MODE_ECB)
truekey=key.decrypt(akey)
print(truekey)

"""方法二"""
k=pyDes.triple_des(api_data,pyDes.ECB,"\0\0\0\0\0\0\0\0",pad=None, padmode=pyDes.PAD_NORMAL)
d=base64.b64decode(appKey)
e=k.decrypt(d,padmode=pyDes.PAD_NORMAL)
print(e)
