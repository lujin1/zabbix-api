#coding=utf-8
from Tkinter import *
import tkinter.messagebox
from zabbix_user import *

master = Tk()
master.title("添加用户")
master.geometry('600x400')  # 是x 不是*
var = IntVar()
var2 = IntVar()

Label(master, text="添加ZABBIX用户",height=3,width=13,fg='blue').grid(row=0, column=1)
Label(master, text="用户组: ").grid(sticky=W)
Label(master, text="账号: ").grid(sticky=W)
Label(master, text="名字: ").grid(sticky=W)
Label(master, text="密码: ").grid(sticky=W)
Label(master, text="邮箱: ").grid(sticky=W)
Label(master, text="手机: ").grid(sticky=W)
Label(master, text=" ").grid(row=7, column=2)

e1 = Entry(master,width = 50)
e2 = Entry(master,width = 50)
e3 = Entry(master,width = 50)
e4 = Entry(master,width = 50)
e5 = Entry(master,width = 50)
e6 = Entry(master,width = 50)


e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=3, column=1)
e4.grid(row=4, column=1)
e5.grid(row=5, column=1)
e6.grid(row=6, column=1)


# checkbutton = Checkbutton(master, text='email', variable=var)
# checkbutton.grid(columnspan=2, sticky=W)

def get():
    o = e1.get()
    print o
def buttonClick():
    usrgrp = e1.get()
    alias = e2.get()
    name = e3.get()
    passwd = e4.get()
    email = e5.get()
    sms = e6.get()
    print u"用户组:%s \n 账号:%s \n 名字:%s \n 密码:%s 邮箱:%s \n 手机:%s" %(usrgrp, alias, name, passwd, email, sms)
    # result.delete(0)
    # Label(master, text="添加ZABBIX用户中......", height=2, width=13, fg='red').grid(row=9, column=1)
    if usrgrp and alias and name and passwd and email and sms:
        zabbix = zabbix_api()
        usrgrpid = zabbix.get_usergroup(usrgrp)
        print u"开始添加"
        result = zabbix.user_create(usrgrpid, alias, name, passwd, email, sms)
        print result
        print  u"---结束----"
         # a = usrgrp + alias + name + passwd + email + sms
        tkinter.messagebox.showinfo(title='添加用户结果', message=result)
    else:
        out = "请补全所填信息！！！"
        print out
        tkinter.messagebox.showinfo(title='添加用户结果', message=out)

button1 = Button(master, text='确定', bg="green",command=buttonClick)
button1.grid(row=8, column=1)
result = Entry(master)


# button2 = Button(master, text='Zoom out')
# button2.grid(row=2, column=2)

mainloop()