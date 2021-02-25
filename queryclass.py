# -*- coding: utf-8 -*-
import os
import sqlite3
import tkinter.ttk
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog
import datetime
import platform
import xlrd
import xlwt
from xlutils.copy import copy 
import framebaseclass
from datatrans import locate_line,change_data_format,write_in_txt,compare_file

class query(framebaseclass.baseFrame):

    def __init__(self,master,user,framename):   
              self.top=master
              self.user=user
              self.framename=framename
              super( ).__init__(self.top,self.user,self.framename)
              self.listbox_raw_file=tkinter.Listbox(self.top)
              self.listbox_raw_file.place(relx=0.0,rely=0.05,relwidth=0.65,height=20)              
              self.buttonrawfile=tkinter.Button(self.top,text="选择原始文件",command=self.choose_raw_file)
              self.buttonrawfile.place(relx=0.7,rely=0.05,width=130,height=20)
              self.listbox_modified_file=tkinter.Listbox(self.top)
              self.listbox_modified_file.place(relx=0.0,rely=0.25,relwidth=0.65,height=20)              
              self.buttonmodifiedfile=tkinter.Button(self.top,text="选择已修改文件",command=self.choose_modified_file)
              self.buttonmodifiedfile.place(relx=0.7,rely=0.25,width=130,height=20)

              '''self.button_compare=tkinter.Button(self.top,text="文件对比",command=self.compare_file)
              self.button_compare.place(relx=0.7,rely=0.45,width=130,height=20)'''

              self.button_excel=tkinter.Button(self.top,text="生成EXCEL",command=self.insert_excel_file)
              self.button_excel.place(relx=0.7,rely=0.65,width=130,height=20)

    def trans_to_txtname(self,filename):#文件转换成txt格式
            file_dir=os.path.dirname(filename)
            raw_name=os.path.basename(filename).split(".")[0]
            txt_name=".".join([raw_name,"txt"])
            abs_txt_dir=os.path.join(file_dir,txt_name)
            return abs_txt_dir

    def trans_file_data(self,filename):#数据转换
            start=locate_line(filename,"<START>")  #开始行
            end=locate_line(filename,"<END>") #10#
            datas=change_data_format(filename,start,end) #转换的数据列表
            txt_file_abs=self.trans_to_txtname(filename)
            write_in_txt(txt_file_abs,datas)
            
        
    def choose_raw_file(self):
            b =tkinter.filedialog.askopenfilename()
            print("b",b)
            self.listbox_raw_file.insert(0,b)
            file_suffix=b.split(".")[-1]
            print("file_suffix",file_suffix)
            if file_suffix=="wld":
                self.trans_file_data(b)
                messagebox.showinfo('原始数据转换', '已转换')
            else:
                messagebox.showwarning('警告', '您选择了错误的文件后缀!')
            #return self.trans_file_data(b)
  
    def choose_modified_file(self):
            b =tkinter.filedialog.askopenfilename()
            self.listbox_modified_file.insert(0,b)
            file_suffix=b.split(".")[-1]
            print("file_suffix",file_suffix)
            if file_suffix=="wlr":
                self.trans_file_data(b)
                messagebox.showinfo('修正数据转换', '已转换')
            else:
                messagebox.showwarning('警告', '您选择了错误的文件后缀!')


    def insert_excel_file(self): #生成excel
        if(platform.system()=='Linux'):
            excel_master = ''.join([os.getcwd(),"/excel模板/模板.xls"])
        else:
            excel_master = ''.join([os.getcwd(),"\excel模板\模板.xls"])
        #print("excel",excel_master)
        template_data = xlrd.open_workbook(excel_master,formatting_info = True)
        #table = data.sheet_by_name("form")
        new_excel = copy(template_data)
        ws = new_excel.get_sheet("form")        
        style = xlwt.XFStyle()
        borders = xlwt.Borders() #初始化单元格边框
        borders.top = 1#上,THIN代表是细线,也可以设置为粗线等样式
        borders.bottom = 1 #下
        borders.left = 1#左
        borders.right = 1#右
        '''borders.left_colour = 10
        borders.right_colour = 11
        borders.bottom_colour = 12
        borders.top_colour = 13'''
        style.borders = borders #将边框样式添加到style样式
        #新建对齐样式
        alignment = xlwt.Alignment() #初始化对齐样式
        alignment.horz = xlwt.Alignment.HORZ_CENTER #水平中心对齐
        alignment.vert = xlwt.Alignment.VERT_CENTER #垂直中心对齐
        style.alignment = alignment #将对齐样式添加到style样式
        
        differents=self.compare_file() #对比文件不同点
        if differents:
           row_start=3           
           for dif in differents:
               ws.write(row_start, 0, dif[0],style)
               ws.write(row_start, 1, dif[1],style)
               ws.write(row_start, 2, dif[2],style)
               ws.write(row_start, 3, dif[3],style)
               row_start+=1               
           ws.set_name(str(dif[0])[0]+"月份")
           new_excel.save('每月水位数据修正表.xls')
           messagebox.showinfo('excel报告', '报告已生成')
        else:
           messagebox.showinfo('无数据', '没有数据')
      
    
    
    def compare_file(self): #对比文件不同点      
        get_raw=self.listbox_raw_file.get(0, END)[0]
        txt_raw_file=self.trans_to_txtname(get_raw)
        get_modified=self.listbox_modified_file.get(0, END)[0]
        txt_modified_file=self.trans_to_txtname(get_modified)
        print(txt_raw_file,txt_modified_file)
        differ=compare_file(txt_raw_file,txt_modified_file)
        data_to_excel=[]
        if len(differ) == 0:
            print('两个文件一样')
        else:
            print('两个文件共有%d处不同' % len(differ))
            for each in differ:
                #print('第%s行不同\n'%str(each[0]),"原:%s"%each[1],"修:%s"%each[2])
                raw=each[1].split(",")
                day=raw[0][-3:]
                time_raw=raw[1]
                time= "".join([time_raw[0:2],":",time_raw[-2:]])
                data_raw="{0:.2f}".format(float(int(raw[2])/100))
                modified=each[2].split(",")                
                data_modified="{0:.2f}".format(float(int(modified[2])/100))
                data_to_excel.append([int(day),time,float(data_raw),float(data_modified)])
        #print(data_to_excel)               
        return data_to_excel
                
                                      
if __name__ =="__main__":
    
     root= Tk()
     query(root,"usertest","frame")
     root.mainloop()


