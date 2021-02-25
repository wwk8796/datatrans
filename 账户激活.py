# -*- coding: utf-8 -*-
'''
激活功能
'''
#from tkinter import *
import tkinter
import tkinter.ttk
import sqlite3
import tkinter.messagebox as messagebox
import time


class Active:    #登录界面    
    def __init__(self, master):
          self.root = master
          width=500
          height=300
          screenwidth =  self.root .winfo_screenwidth()
          screenheight =  self.root .winfo_screenheight()
          alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
          self.root.geometry(alignstr)
          self.root.title('激活功能')
          self.var_M=self.get_users()  #["M001","M002","M003","M004","M005","M006","M007","M008"]
          #print(self.get_users())
          self.page = tkinter. Frame(self.root)
          self.creatapage()
          
    def creatapage(self):  #界面布局
          label_user=tkinter.Label(self.root,text="选择用户名:")
          label_user.place(relx=0.3,rely=0.05,width=100,height=30)
          self.combo_user=tkinter.ttk.Combobox(self.root,value=tuple(self.var_M))
          self.combo_user.place(relx=0.49,rely=0.05,width=100,height=30)
          button_active= tkinter.Button(self.root, text="激活账户", command=self.active_action) #
          button_active.place(relx=0.3,rely=0.25,width=100,height=40)
          button_deactive= tkinter.Button(self.root, text="关闭账户", command=self.deactive_action) #
          button_deactive.place(relx=0.5,rely=0.25,width=100,height=40)
          button_deactive= tkinter.Button(self.root, text="删除账户", command=self.delete_action) #
          button_deactive.place(relx=0.7,rely=0.25,width=100,height=40)

    def get_users(self):  #初始化得到用户清单
           self.conn=sqlite3.connect("database.db")
           c=self.conn.cursor()
           sql="SELECT Username From user_info "
           #print(sql)
           c.execute(sql)
           li=c.fetchall()
           result_list=[ ]
           for i in li:
                 result_list.append(i[0])               
           self.conn.commit()
           self.conn.close()
           return result_list

    def get_signal(self,user):
          self.conn=sqlite3.connect("database.db")
          c=self.conn.cursor()          
          sql="SELECT isActive From user_info Where Username ='%s'"%user
          #print(sql)
          c.execute(sql)
          li=c.fetchone()
          self.conn.commit()
          self.conn.close()
          return li


    def update_status(self,user,status="Y"):  #更新用户状态
            self.conn=sqlite3.connect("database.db")
            c=self.conn.cursor()
            sql="UPDATE user_info SET isActive='%s' Where Username = '%s'"%(status,user)
            #print(sql)
            c.execute(sql)
            self.conn.commit()
            self.conn.close()
  
           
    def active_action(self):          
           try:
               user=self.combo_user.get()          
               s=self.get_signal(user)
               #print(s)
               if s[0]=="N":
                     self.update_status(user)
                     messagebox.showinfo('操作完成', '用户已激活')
               else:
                     messagebox.showwarning('警告', '用户已激活!')                             
           except (Exception) as e:
                     messagebox.showerror('错误', e)
                 
    def deactive_action(self):          
           try:
               user=self.combo_user.get()          
               s=self.get_signal(user)
               #print(s)
               if s[0]=="Y":
                     self.update_status(user,status="N")
                     messagebox.showinfo('操作完成', '用户已关闭!')
               else:
                     messagebox.showwarning('警告', '用户已关闭!')                             
           except (Exception) as e:
                     messagebox.showerror('错误', e)
                 

    def delete_action(self):
           user=self.combo_user.get()
           self.conn=sqlite3.connect("database.db")
           c=self.conn.cursor()          
           sql="DELETE  From user_info Where Username ='%s'"%user
           #print(sql)
           c.execute(sql)
           li=c.fetchone()
           self.conn.commit()
           self.conn.close()
           messagebox.showinfo('操作完成', '用户已删除!')



                     


if __name__ == '__main__':
    root = tkinter.Tk()
    Active(root)
    root.mainloop()
