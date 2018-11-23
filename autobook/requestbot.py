# -*- coding: utf-8 -*-

import requests
import io
import datetime
from PIL import Image, ImageTk
import json
from bs4 import BeautifulSoup
from time import time,ctime, sleep

def get_date_list(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    print(date_list)
    return date_list

class Bot(object):
    """docstring for Hotel"""
    def __init__(self):
        self.session = requests.Session()
        self.all_question={}
        self.book_data = {}

    def get_code(self):
        main_url = 'http://bsdt.baoan.gov.cn/login.jspx?locale=zh_CN'
        res = self.session.get(main_url)
        t_str = str(time()).replace('.','')
        url ='http://bsdt.baoan.gov.cn/captcha.svl?d='+t_str
        res = self.session.get(url)
        data_stream = io.BytesIO(res.content)
        # open as a PIL image object
        pil_image = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image

    # usertype: 1
    # username: qqqeeebbb
    # password: Zwx535666
    # captcha_org: ovbb
    # captcha: 651517
    # ovbb
    # returnUrl: /member/index.jspx
    def Login(self,uname,pswd,code):
        url ='http://bsdt.baoan.gov.cn/caLogin.jspx'
        url ='http://bsdt.baoan.gov.cn/login.jspx'
        data ={}
        data['usertype'] = 1
        data['username']=uname
        data['password']=pswd
        data['captcha_org'] = code
        val_url ='http://bsdt.baoan.gov.cn/captcha/syncvalidate.jspx?captcha='+code
        val_res = self.session.get(val_url)
        data['captcha'] = json.loads(val_res.content)["valivalue"]
        data['returnUrl'] = '/member/index.jspx'
        print(data)
        res = self.session.post(url,data)
        #print(res.content.decode('utf-8'))
        if res.url == "http://bsdt.baoan.gov.cn/member/enterpriseIndexgr.jspx?sxid=&locale=zh_CN":
            return True
        return False

    def get_bookinfo(self):
        book_info ={}
        select_dict ={}
        res = self.session.get("http://bsdt.baoan.gov.cn/member/reservation_add_new_xf.jspx")
        search_soup = BeautifulSoup(res.text, 'html.parser')
        select_list = search_soup.select('#res_sxid option')
        for item in select_list:
            show_text = item.text.strip()
            #print(show_text)
            select_dict[show_text] = item.get('value')
        book_info["select"] = select_dict

        name_tag = search_soup.select_one('#res_name')
        name =name_tag.get('value')
        book_info["name"] = name

        id_tag = search_soup.select_one('#res_card')
        id = id_tag.text
        book_info["id"] = id

        phone_tag = search_soup.select_one('#res_phone')
        phone = phone_tag.get('value')
        book_info["phone"] = phone

        sdate_tag = search_soup.select_one('#startDate')
        sdate = sdate_tag.get('value')
        book_info["sdate"] = sdate

        edate_tag = search_soup.select_one('#endDate')
        edate = edate_tag.get('value')
        book_info["edate"] = edate

        deptid_tag = search_soup.select_one('#res_deptid')
        deptid = deptid_tag.get('value')
        book_info["deptid"] = deptid
        self.book_data = book_info
        print(book_info)

        return book_info

    # createdate: 2018-01-25
    # deptId: 007542689
    # cardid: 142243444443773337
    # phone: 18811111111
    # {"am":"0","pm":"0","code":"0"}
    def check_book_state(self,para):
        success =False
        check_info= []
        #self.get_bookinfo()
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=6)
        n_days = now + delta

        datelist = get_date_list(now.strftime('%Y-%m-%d'),n_days.strftime('%Y-%m-%d'))

        date_req_url = 'http://bsdt.baoan.gov.cn/member/getBATimeByDate.jspx'
        data = {}
        data['deptId'] = self.book_data["deptid"]
        data['cardid'] = self.book_data["id"]
        data['phone'] = self.book_data["phone"]
        for date in datelist:
            data['createdate'] = date
            res = self.session.post(date_req_url,data)
            print(res.content)
            print(res.content.decode('utf-8'))
            date_info = {}
            date_info["date"] = date
            try:
                am_left = int(json.loads(res.content)["am"])
                pm_left = int(json.loads(res.content)["pm"])
                date_info["am"] = am_left
                date_info["pm"] = pm_left
                if am_left > 0:
                    success = self.book(date,1,para)
                    if success:
                        date_info["success"] = [date, "上午"]
                        check_info.append(date_info)
                        break
                elif pm_left >0:
                    success = self.book(date, 2,para)
                    if success:
                        date_info["success"] = [date, "下午"]
                        check_info.append(date_info)
                        break
                else:
                    check_info.append(date_info)
            except:
                print("date_req_url error")



        print(check_info)
        return check_info, success

    #参数
    #type A
    #res_sxid 预约事项
    #res_deptid  007542689
    #res_name 名字
    #res_pid  证件号
    #res_phone 电话
    #res_gcmc  字符串
    #res_gcdz  字符串
    #startTime  2018-01-21
    #endDate    2018-01-25
    #createtime 2018-01-25
    #content  上午1 下午2

    #para{'res_perm': '12126900158009622014440306', 'gcmc': 'asdsada ', 'gcdz': 'asdsadsad'}
    def book(self,createtime,content,para):
        book_url = "http://bsdt.baoan.gov.cn/member/reservation_save_ba.jspx"
        data={}
        data["type"] = "A"
        data["res_sxid"] = para["res_perm"]
        data["res_deptid"] = "007542689"
        data["res_name"] = self.book_data["name"]
        data["res_pid"] = self.book_data["id"]
        data["res_phone"] = self.book_data["phone"]
        data["res_gcmc"] = para["gcmc"]
        data["res_gcdz"] = para["gcdz"]
        data["startTime"] = self.book_data["sdate"]
        data["endDate"] = self.book_data["edate"]
        data["createtime"] = createtime
        data["content"] = content
        print(data)
        res = self.session.post(book_url,data)

        print(res.url)
        print(res.text)
        if res.url=="http://bsdt.baoan.gov.cn/member/reservation_save_ba.jspx":
            return False


        return True

bot = Bot()