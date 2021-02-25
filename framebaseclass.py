# -*- coding: utf-8 -*-
import os

from tkinter import *
import datetime
#import baseclass

class baseFrame:                
         def __init__(self, master,user,framename):
              self.root = master
              self.user=user
              self.framename=framename
              #self.root.resizable(0,0)
              self.root.title(self.framename+self.user)
              width =800
              height = 500
              screenwidth = self.root.winfo_screenwidth()
              screenheight = self.root.winfo_screenheight()
              alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
              self.root.geometry(alignstr)
              #self.root.iconbitmap(".\\pic\\smart.ico")
              self.root.wm_attributes("-topmost", 1)
              #self.photo_back = PhotoImage(file=os.getcwd()+".\\pic\\back.png")
              #self.photo0 = PhotoImage(file=os.getcwd()+".\\pic\\we1.png")
              self.baseframe_ui()
              
         def baseframe_ui(self):
              self.one = Label(self.root, text="© Powered by companyname "+"2021-"+str(datetime.datetime.now().year), width=60, height=2, font=("Arial", 10))
              self.one.pack(side=BOTTOM)
              #self.fx=LabelFrame(self.root)
              #self.fx.place(relx=0.1,rely=0.88,relwidth=0.1,relheight=0.12)           
              #self.theLabel = Label(self.fx,image=self.photo0,fg="white")
              #self.theLabel.pack()
              #self.button_back=Button(self.root,image=self.photo_back,command=self.back)
              #self.button_back.place(relx=0.0,rely=0.88)
              
         def back(self):
                pass
                                       
if __name__ == '__main__':
    root = Tk()
    baseFrame(root,"usertest","模板测试")
    root.mainloop()


