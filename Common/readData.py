#coding=utf-8

"""通过readlines()读取文件"""

import random,os,re

datapath=os.path.join(os.path.dirname(os.path.relpath(__file__)),"phone.txt")
phonepath=os.path.join(os.path.dirname(os.path.realpath(__file__)),'login.txt')
class ReadData():
    #随机数放在init方法中，保证只获取一次随机数，因为类只实例化一次
    def __init__(self):
        with open(datapath) as f:
            phone=f.readlines()
        self.ran=random.randint(0,len(phone)-1)

    def readPhoneNumber(self):
        with open(datapath) as f:
            phone=f.readlines()
        phones=[]
        for i in phone:
            #通过正则过滤字符串中的非数字字符
            j=re.sub("\D","",i)
            phones.append(j)
        phone=phones.pop(int(self.ran))
        os.remove(datapath)
        for i in phones:
            with open(datapath,'a') as f:
                f.truncate()
                f.write(i+'\n')
        with open(phonepath,'a') as f:
            f.write(phone+'\n')
        return int(phone)

    def account(self):
        s=[]
        with open(phonepath,'r') as f:
            a=f.readlines()
        for i in a:
            j=re.sub('\D','',i)
            s.append(j)
        return int(s[random.randint(0,len(s)-1)])

    def phone(self):
        s=[]
        with open(datapath,'r') as f:
            a=f.readlines()
        for i in a:
            j=re.sub('\D','',i)
            s.append(j)
        return int(s[self.ran])


# if __name__=='__main__':
#     read=ReadData().readPhoneNumber()
#     print(read)








