#coding=utf-8

import random,requests,json

host='https://api1.fjdaily.com'
class common():
    """获取栏目数据"""
    def article_columns(self):
        params={
            "parentColumnId":"1",
            "siteId":"1",
            "debug":"true"
        }
        url=host+'/app_if/getColumnsAll'
        s=requests.session()
        req=s.get(url,params=params)
        js=json.loads(req.content)
        cols=js["columns"]
        newcols=[]
        for i in cols:
            newcols.append(i["columnId"])
        return newcols[random.randint(0,len(newcols)-1)]

    """获取栏目列表稿件数据"""
    def article_lists(self,colid):
        # colid=common().articlecolumns()
        params={
            "columnId":str(colid),
            "siteId":"1",
            "debug":"true"
        }
        url=host+'/app_if/getArticles'
        s=requests.session()
        req=s.get(url,params=params)
        js=json.loads(req.content)
        fids=js["list"]
        print(fids)
        fileids=[]
        for i in fids:
            fileids.append(i["fileId"])
        print(fileids)
        return fileids[random.randint(0,len(fileids)-1)]

    """获取活动列表数据"""
    def activity_list(self):
        params={
            "catID":"-1",
            "siteID":"1",
            "debug":"true"
        }
        url=host+'/app_if/activityList'
        s=requests.session()
        req=s.get(url,params=params)
        js=json.loads(req.content)
        l=js["list"]
        list=[]
        for i in l:
            list.append(i["fileId"])
        return list[random.randint(0,len(list)-1)]





#
# if __name__=="__main__":
#     print(common().article_lists(231))
