# -*- coding: utf-8 -*-
'''
注册和登入页面
'''
import os
import platform
from tkinter import *
import sqlite3
import tkinter.messagebox as messagebox
import time
from PIL import Image, ImageTk
import queryclass

class LoginPage:    #登录界面
    
    def __init__(self, master):
          self.root = master
          width=500
          height=300
          screenwidth =  self.root .winfo_screenwidth()
          screenheight =  self.root .winfo_screenheight()
          alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
          self.root.geometry(alignstr)
          #self.root.iconbitmap(''.join([os.getcwd(),"/pic/smart.ico"]))
          if(platform.system()=='Linux'):
            im = Image.open(''.join([os.getcwd(),"//pic//smart.ico"]))
          else:
            im = Image.open(''.join([os.getcwd(),"\\pic\\smart.ico"]))
          #im = Image.open("smart.ico")
          img = ImageTk.PhotoImage(im)
          self.root.tk.call('wm', 'iconphoto', root._w, img)
          #self.root.iconbitmap("smart.ico")
          self.root.title('数据管理')          
          self.username = StringVar()
          self.password = StringVar()
          self.page = Frame(self.root)
          self.creatapage()
          
    def creatapage(self):  #界面布局
          Label(self.page).grid(row=0)
          Label(self.page, text='用户名:').grid(row=1, stick=W, pady=10)
          Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
          Label(self.page, text='密码:').grid(row=2, stick=W, pady=10)
          Entry(self.page, textvariable=self.password, show='*').grid(row=2, stick=E, column=1)
          Button(self.page, text='  登录  ', command=self.login).grid(row=3, stick=W, pady=10)
          Button(self.page, text='注册账号', command=self.register).grid(row=3, stick=E, column=1)
          self.page.pack()
          
    def add_error(self,user,num):  
          self.conn=sqlite3.connect("database.db")
          c=self.conn.cursor()
          #sql="UPDATE user_info SET error="+str(num)+" Where Username ="+user
          sql="UPDATE user_info SET error='%s' Where Username ='%s' "%(str(num),user)
          #print(sql)
          c.execute(sql)
          li=c.fetchone()
          self.conn.commit()
          self.conn.close()
          return li
        
    def login(self):  #登录功能
          self.conn = sqlite3.connect('database.db')
          curs = self.conn.cursor()
          query = "select Username,Password,error,isActive from user_info where Username='%s'" % self.username.get()
          curs.execute(query)  # 返回一个迭代器
          c = curs.fetchall()  # 接收全部信息
          if len(c) == 0:
              #self.root.withdraw()
              messagebox.showerror('登录失败', '账户不存在')
              self.root.deiconify()
          else:
                us, pw, error,isActive= c[0]
                if isActive=="N":
                   messagebox.showwarning('登录失败', '用户还未激活!')
                   self.root.deiconify()
                else:
                    if  error >= 3:
                          messagebox.showwarning('登录失败', '错误超过三次账户已被锁定')
                          self.root.deiconify()
                    elif us == self.username.get() and pw == self.password.get():
                          date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                          #sql="UPDATE user_info SET Logindate="+"'"+date+"'"+ " WHERE Username='%s'"%us
                          sql="UPDATE user_info SET Logindate='%s' ,error=0  WHERE Username='%s'"%(date,us)
                          curs.execute(sql)
                          self.conn.commit()
                          self.conn.close()                   
                          self.root.destroy()
                          root1=Tk()
                          queryclass.query(root1,us,"数据处理")
                    else:
                           messagebox.showwarning('登录失败', '密码错误')
                           num=int(error)+1
                           self.add_error(us,num) #更新错误次数
                           self.root.deiconify()

    def register(self): #注册功能跳转
          self.page.destroy()
          RegisterPage(self.root)

 
class RegisterPage:  #注册界面
    
    def __init__(self, master=None):
          self.root = master
          self.root.title('账号注册')
          width=500
          height=300
          screenwidth =  self.root .winfo_screenwidth()
          screenheight =  self.root .winfo_screenheight()
          alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
          self.root.geometry(alignstr)
          if(platform.system()=='Linux'):
            im = Image.open(''.join([os.getcwd(),"//pic//smart.ico"]))
          else:
            im = Image.open(''.join([os.getcwd(),"\\pic\\smart.ico"]))
          #im = Image.open("smart.ico")
          img = ImageTk.PhotoImage(im)
          self.root.tk.call('wm', 'iconphoto', root._w, img)
          #self.root.iconbitmap(".\\pic\\smart.ico")
          self.username = StringVar()
          self.password0 = StringVar()  # 第一次输入密码
          self.password1 = StringVar()  # 第二次输入密码
          self.email = StringVar()
          self.page = Frame(self.root)
          self.createpage()
          
    def createpage(self): #界面布局
          Label(self.page).grid(row=0)
          Label(self.page, text="工号:").grid(row=1, stick=W, pady=10)
          Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
          Label(self.page, text="密码:").grid(row=2, stick=W, pady=10)
          Entry(self.page, textvariable=self.password0, show='*').grid(row=2, column=1, stick=E) 
          Label(self.page, text="再次输入:").grid(row=3, stick=W, pady=10)
          Entry(self.page, textvariable=self.password1, show='*').grid(row=3, column=1, stick=E)
          Label(self.page, text="Email*:").grid(row=4, stick=W, pady=10) 
          Entry(self.page, textvariable=self.email).grid(row=4, column=1, stick=E)
          Button(self.page, text="  返回  ", command=self.repage).grid(row=5, stick=W, pady=10)
          Button(self.page, text="  注册  ", command=self.register).grid(row=5, column=1, stick=E)
          self.page.pack() 

    def repage(self):  #返回登录界面"
          self.page.destroy()
          #self.conn.close()
          LoginPage(self.root)
          
    def create_db(self):
          self.conn=sqlite3.connect("database.db")
          c=self.conn.cursor()
          content="id INTEGER PRIMARY KEY AUTOINCREMENT ,Registerdate DATE,Email TEXT,Username TEXT,Password TEXT,isActive TEXT,error INTEGER,Logindate DATE"   #拼接字段语句
          sql="CREATE TABLE IF NOT EXISTS user_info"+"("+content+")"
          #print(sql)
          c.execute(sql)
          self.conn.commit()
          self.conn.close()
          
    def get_user(self,user):
          self.conn=sqlite3.connect("database.db")
          c=self.conn.cursor()          
          sql="SELECT Username From user_info Where Username ='%s'"%user
          #print(sql)
          c.execute(sql)
          li=c.fetchone()
          self.conn.commit()
          self.conn.close()
          return li

    def register(self):  #注册
          if   self.password0.get() != self.password1.get():
               messagebox.showwarning('错误', '密码核对错误')
               self.root.deiconify()
          elif len(self.username.get()) == 0 or len(self.password0.get()) == 0 or len(self.email.get()) == 0:
                messagebox.showerror("错误", "不能为空")
                self.root.deiconify()
          elif len(self.password0.get())<6:
                messagebox.showerror("错误", "密码长度至少六位")
                self.root.deiconify()
          else:
                  self.create_db()   #没有数据库的话先创建
                  exist=self.get_user(self.username.get())  #是否存在用户
                  if exist:
                      messagebox.showerror("错误", "用户名已存在")
                      self.root.deiconify()
                  else:
                      self.conn = sqlite3.connect('database.db')
                      curs = self.conn.cursor()
                      date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                      content="Registerdate,Username ,Password ,Email ,isActive,error,Logindate "
                      val=[date,self.username.get(), self.password0.get(), self.email.get(),'N', 0,date]
                      sql="INSERT INTO user_info" +chr(32)+ "("+content+")"+chr(32)+"VALUES(?,?,?,?,?,?,?)"    
                      try:              
                        curs.execute(sql, val)
                        self.conn.commit()
                        self.conn.close()
                        messagebox.showinfo("成功", "注册成功，按确定返回登录界面")
                        self.page.destroy()
                        LoginPage(self.root)
                      except sqlite3.IntegrityError:
                            pass
                    


if __name__ == '__main__':
    root = Tk()
    LoginPage(root)
    root.mainloop()
