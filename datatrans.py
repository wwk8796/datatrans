from datetime import datetime

def locate_line(filename,mark_name):   #定位起始行
    with open(filename, "r") as f:  # 打开文件
        #data = f.read()
        lines = f.readlines()
        num=-1
        for line in lines:
            location=line.count(mark_name)
            num+=1
            if location:
                return num

        
    

def change_data_format(filename,start,end):  #数据转换
   with open(filename, "r") as f:  # 打开文件
    data = f.readlines()
    #print(data[2].split()[0].split("/"))
    list_date_collect=data[2].split()[0].split("/")
    year=list_date_collect[0]
    day="".join(list_date_collect[1:])
    trans_list=[]   
    for i in data[start+1:end]:
        to_str=' '.join(i.split())
        line_content_list=to_str.split()
        date_str=line_content_list[0] #字符窜
        date_format="".join(date_str.split("/"))
        #print(date_format)
        if int(day)<int(date_format):
           final_date="".join([str(20)+str(int(year)-1),date_format])  #前一年
        else:
           final_date="".join([str(20)+year,date_format]) #当年
        time_str=line_content_list[1]
        time_format="".join(time_str.split(":"))  #时间格式        
        data_detail=line_content_list[2:]#数据取值        
        j=0
        for d in data_detail:            
            final_data_detail='%06d' %int(float(d)*100)
            final_time_format='%04d'%int(int(time_format)+j)
            #print(final_date,final_time_format,final_data_detail)
            trans_list.append(','.join([final_date,final_time_format,final_data_detail]))
            j+=5
    return trans_list




def write_in_txt(filename,datas): #写入数据
    with open(filename,"w") as f:         
         for data in datas:
             #print(data)
             f.write(data+"\n")


def compare_file(file1,file2):
    f1=open(file1,'r')
    f2=open(file2,'r')
    count = 0
    diff = []
    for line1 in f1:
        line2 = f2.readline()
        count +=1
        if line1 != line2:
            #diff.append('第%s行不同'%str(count)+"\n"+"原:"+line1+"修:"+line2)
            diff.append([str(count),line1,line2])
    f1.close()
    f2.close()
    return diff             

if __name__ == "__main__":
   start=locate_line("634017502021.wlr","<START>")  #开始行
   end=locate_line("634017502021.wlr","<END>") #10#
   #print(change_data_format("L01750A1.wld",start,end))
   datas=change_data_format("634017502021.wlr",start,end)
   write_in_txt("text1.txt",datas)


