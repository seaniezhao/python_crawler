
# -*- coding: utf-8 -*-
import requests
from time import time,ctime, sleep
import json

class Bot(object):
    """docstring for Hotel"""
    def __init__(self,uname,pswd):
        self.uname = uname
        self.pswd = pswd
        self.cookies = {}
        self.all_question={}

    def answer_q(self):
        l_url = 'http://zzb.d2sw.cn/sx-answer/pclogin?telphone=%s&password=%s' % (self.tel, self.pswd)
        res = requests.get(l_url)

        self.cookies["p-token"] = json.loads(res.content)["data"]
        self.cookies["path"] = "/"

        #个人资料
        #res = requests.get('http://lx.djfy365.com/sx-answer/pc/personal',cookies=self.cookies)

        #到答题页
        res = requests.get('http://zzb.d2sw.cn/sx-answer/pc/questions', cookies=self.cookies)

        #所有问题
        res = requests.get('http://zzb.d2sw.cn/sx-answer/pc/questions/data', cookies=self.cookies)
        self.all_question = json.loads(res.content)["data"]["data"]

        resA = []
        for question in self.all_question:
            all_ans = question["ans"]
            for ans in all_ans:
                if ans["valid"] ==1 :
                    resA.append(str(ans["id"]))

        sleep(150)
        #提交答案
        d = {}
        d["answers[]"] = resA
        d_str = json.dumps(d)
        print (d_str)
        res = requests.post('http://zzb.d2sw.cn/sx-answer/pc/result', data=d , cookies=self.cookies)

        res = requests.get('http://zzb.d2sw.cn/sx-answer/pc/personal', cookies=self.cookies)

        return res.content


# account = [["15364880705","123456"],["15364541121","665241"],["18665374383","zhangjianlin"],["17722642405","zhangjianlin1"],["15122212600","zhangjian"],["13035112391","huowendong"],["15986842021","donglu"],["18676365356","196489284"]]
# for arg in account:
#     bot = Bot(arg[0],arg[1])
#     try:
#         txt=bot.answer_q()
#     except:
#         print (arg[0]+"执行异常")

s = requests.Session()
res = s.get('http://bsdt.baoan.gov.cn/member/reservation_add_new_xf.jspx')

print(res.content.decode('utf-8'))


print(time())