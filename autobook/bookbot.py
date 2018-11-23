# -*- coding: utf-8 -*-
import time as tm
from tkinter import *
from requestbot import *
from tkinter.messagebox import *
from tkinter import ttk
import threading


class LoginPage(Frame):
    def __init__(self):
        super().__init__()
        self.username = StringVar()
        self.password = StringVar()
        self.username.set("mercy2018")
        self.password.set("********")

        self.code = StringVar()
        self.code_pic = bot.get_code()
        self.pack()
        self.createForm()


    def createForm(self):
        Label(self).grid(row=0, stick=W, pady=10)
        Label(self, text='账户: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self, text='密码: ').grid(row=2, stick=W, pady=10)
        #, show='*'
        Entry(self, textvariable=self.password).grid(row=2, column=1, stick=E)
        self.code_label = Label(self, image=self.code_pic , bg='brown')
        self.code_label.grid(row=3, stick=W, pady=10)
        Label(self, text='验证码: ').grid(row=4, stick=W, pady=10)
        self.code_input = Entry(self, textvariable=self.code)
        self.code_input.grid(row=4, column=1, stick=E)
        Button(self, text='登陆', command=self.loginCheck).grid(row=5, stick=W, pady=10)
        Button(self, text='退出', command=self.quit).grid(row=5, column=1, stick=E)


    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        code = self.code.get()
        success = bot.Login(name,secret,code)
        if success:
            self.destroy()
            MainPage()
        else:
            showinfo(title='登录失败', message='账号/密码错误或者请检查网络')
            #self.username=""
            #self.password=""
            self.code = StringVar(self,"")
            self.code_input.config(textvariable=self.code)
            self.code_pic = bot.get_code()
            self.code_label.config(image=self.code_pic)


class MainPage(Frame):
    def __init__(self):
        super().__init__()
        self.list_var = StringVar()
        # self.name = StringVar()
        # self.id = StringVar()
        # self.phone = StringVar()
        self.gcmc = StringVar()
        self.gcdz = StringVar()
        self.select_dict = {}
        self.pack()
        self.createForm()


    def createForm(self):
        try:
            book_info = bot.get_bookinfo()
        except Exception as e:
            showinfo(title='错误', message='网络错误')
            print(e)
            return
        # book_info["select"]={"abc":123,"dsef":456}
        # book_info["name"] = "大声道撒"
        # book_info["id"] = "45645343543sadsads"
        # book_info["phone"] = "4564638768"
        # book_info["sdate"] = "0000-00-00"
        # book_info["edate"] = "0000-00-00"

        Label(self, text='预约事项').grid(row=0, stick=W, pady=6)
        numberChosen = ttk.Combobox(self, width=50, textvariable=self.list_var )
        numberChosen['values'] = tuple(book_info["select"].keys())  # 设置下拉列表的值
        numberChosen.grid(row=0,column=1,stick=W, pady=6)  # 设置其在界面中出现的位置  column代表列   row 代表行
        numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        self.select_dict = book_info["select"]

        Label(self, text='姓名: ').grid(row=2, stick=W, pady=10)
        Label(self, text=book_info["name"]).grid(row=2, column=1, stick=W)
        Label(self, text='证件号: ').grid(row=3, stick=W, pady=10)
        Label(self, text=book_info["id"]).grid(row=3, column=1, stick=W)
        Label(self, text='电话: ').grid(row=4, stick=W, pady=10)
        Label(self, text=book_info["phone"]).grid(row=4, column=1, stick=W)

        Label(self, text='工程名称(大于4字): ').grid(row=5, stick=W, pady=10)
        Entry(self, textvariable=self.gcmc ,width=40).grid(row=5, column=1, stick=W)
        Label(self, text='工程地址(大于4字): ').grid(row=6, stick=W, pady=10)
        Entry(self, textvariable=self.gcdz, width=40).grid(row=6, column=1, stick=W)


        Label(self, text=book_info["sdate"]).grid(row=7, stick=W, pady=10)
        Label(self, text=book_info["edate"]).grid(row=7, column=1, pady=10,stick=W)
        Button(self, text='开始运行', command=self.book).grid(row=10,column=1)

    def book(self):
        self.destroy()

        para ={}

        para["res_perm"] = self.select_dict[self.list_var.get()]
        para["gcmc"] = self.gcmc.get()
        para["gcdz"] = self.gcdz.get()
        print(para)
        BookPage(para)
        pass

class BookPage(Frame):
    def __init__(self, para):
        super().__init__()
        self.msecs = 1000
        self.pack()
        self.para = para
        self.try_time = 0
        self.check_info = None
        self.quit_t = False
        self.createForm()


    def createForm(self):
        Label(self, text='尝试次数').grid(row=1, stick=W, pady=10)
        self.l_try_time = Label(self, text=self.try_time)
        self.l_try_time.grid(row=1, column=1, stick=W)

        Label(self, text='日期').grid(row=2, stick=W, pady=10)
        Label(self, text='上午剩余').grid(row=2, column=1, stick=W, pady=10)
        Label(self, text='下午剩余').grid(row=2, column=2, stick=W, pady=10)

        self.showLabels=[]
        for i in range(5):
            l1 = Label(self, text="yyyy-mm-dd")
            l1.grid(row=i+3, stick=W, pady=10)
            l2 = Label(self, text="-")
            l2.grid(row=i+3, column=1, stick=E, pady=10)
            l3 = Label(self, text="-")
            l3.grid(row=i+3, column=2, stick=E, pady=10)
            self.showLabels.append([l1,l2,l3])


        Button(self, text='取消', command=self.cancel).grid(row=20, column=1)

        self.refresh(1)

    def refresh(self,try_time):
        try:
            check_info, success = bot.check_book_state(self.para)
        except Exception as e:
            showinfo(title='出错了', message="一次网络异常")
            print(e)
            #return

        self.try_time = try_time
        self.check_info = check_info
        self.l_try_time.config(text=self.try_time)

        for i in range(len(self.showLabels)):
            if i<len(self.check_info):
                self.showLabels[i][0].config(text=self.check_info[i]['date'])
                self.showLabels[i][1].config(text=self.check_info[i]['am'])
                self.showLabels[i][2].config(text=self.check_info[i]['pm'])
            else:
                self.showLabels[i][0].config(text="")
                self.showLabels[i][1].config(text="")
                self.showLabels[i][2].config(text="")

        try_time += 1
        if success:
            for info in check_info:
                if "success" in info:
                    s_info = info
            msg = "您已预约到" + s_info["success"][0] + ", " + s_info["success"][1] + "的资格"
            showinfo(title='成功', message=msg)
            return
        elif not self.quit_t:
            self.after(self.msecs, self.refresh,try_time)

    def cancel(self):
        self.quit_t = True
        self.destroy()
        MainPage()


root = Tk()
root.title('智能监测系统')
width = 500
height = 500
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)  # 居中对齐

page1 = LoginPage()
#MainPage()
root.mainloop()






