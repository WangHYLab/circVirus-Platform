# -*- coding: utf-8 -*- 
import openpyxl as op
from openpyxl import Workbook
from openpyxl.styles import Font, Color, colors, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import pandas as pd
import numpy as np
import os

def getGroup(file,group_name="Unknown"):
    group_name="Group: "+group_name
    count=0
    dic={}
    df=[]
    for line in file:
        if line.startswith(group_name):
            count=count+1
            df=[]
        elif line.startswith("Sample"):
            # print(count)
            header=line.strip().split('\t')
        elif line.startswith("1E") and count!=0:
            y=line.strip().split('\t')
            df.append(y)
        elif line.startswith("1E")==False and count!=0:
            # print(df)
            out=pd.DataFrame(df)
            out.index=out[0]
            dic[count]=out
    # A file may end immediately after the last data row, with no trailing
    # non-1E line to trigger the finalization above.
    if count!=0 and df:
        out=pd.DataFrame(df)
        out.index=out[0]
        dic[count]=out
    return(dic)

def getPlateInfo(dic,key=1,print_info=False):
    n=len(dic.keys())
    df=dic[key]
    sample=df[0]
    ten_x=[]
    kong=[]
    for i in sample:
        line=i.split('-')
        ten_x.append(line[1])
        kong.append(line[2])
    k=sorted(list(set(kong)))
    bs=sorted(list(set(ten_x)))
    if(print_info):
        print("Number of Plate:",n)
        print("Number of Sample(10x):",len(bs),"; detail:",bs)
        print("Number of Well",len(k))
    return(n,bs,k)

def checkPlate(dic):
    one=[]
    for i in dic.keys():
        # print(i)
        new=getPlateInfo(dic,key=i)
        if one==[]:
            one=new
        elif one!=[] and one!=new:
            print("The properties of the Plates are inconsistent")
            return False
        elif  i==len(dic.keys()):
            return True

def readFile(file):
    out=open(file,'r',encoding='utf-8')
    return(out)

def checkValue(value,low=85.2,high=4261.8):
    if value=='Range?':
        return "未检出"
    elif float(value)>high:
        return "超上限"
    elif float(value)<low:
        return "未检出"
    else:
        return value

def writeXlsx(wb,ws,out,r,plate):

    result_pd = out #result为处理之后的数据，可以是pivot_table 处理后的数据，也可以是group by 之后的数据
    # result_pd.columns = result_pd.columns.droplevel(0)  # 表头数据转化
    result_pd = result_pd.reset_index()  # 转化index
    col=list(result_pd.columns)
    col[0]="浓度"
    result_pd.columns=col
    result_pd['浓度']=["(1E-"+str(i)+")" for i in list(result_pd['浓度'])]
    columns = result_pd.columns.values #结果数据的表头

    ws.cell(row=r-2, column=1).value = '板'+str(plate) #写入板号
    # ws.merge_cells(f"{get_column_letter(1)}{r-2}:{get_column_letter(len(result_pd.columns))}{r-2}")
    ws.merge_cells("%s%s:%s%s" %(get_column_letter(1),r-2,get_column_letter(len(result_pd.columns)),r-2))
    for line in result_pd.values:
        for col in range(1, len(line) + 1):
            ws.cell(row=r, column=col).value = line[col - 1]
        r += 1

    for col in range(1, len(line) + 1):    
        for j in columns:
            ws.cell(row=r-1-len(result_pd[1]), column=col).value = columns[col-1] #写入表头
    
    #设置单元格样式
    #边框
    border_set = Border(left=Side(style='thin', color=colors.BLACK),  # 左边框
                    right=Side(style='thin', color=colors.BLACK),  # 右边框
                    top=Side(style='thin', color=colors.BLACK),  # 上边框
                    bottom=Side(style='thin', color=colors.BLACK))  # 下边框
    #对齐方式
    for i in ws:
        for j in i:
            j.alignment = Alignment(horizontal='center', vertical='center',wrapText = True)
            j.border = border_set
    #长宽
    width = 12.5
    height = 17
#     height = width * (2.2862 / 0.3612)
    for i in range(2, ws.max_row+1):
        ws.row_dimensions[i].height = height
    for i in range(1, ws.max_column+1):
        ws.column_dimensions[get_column_letter(i)].width = width

    return ws
    
def reportXlsx(dic,out_file="out.xlsx",
               qydbh="",xmbh="",jcbh="",jcxm="",jcyj=""):
    info=getPlateInfo(dic,key=1,print_info=False)
    max_wid=len(info[2])+1
    half_wid=round(max_wid/2)-1
    wb = Workbook()#创建工作簿
    ws = wb.create_sheet('数据', 0)#创建工作表
    #表头
    ws.cell(row=1, column=1).value = "科济生物医药（上海）有限公司检验报告书"
    # ws.merge_cells(f"{get_column_letter(1)}{1}:{get_column_letter(max_wid)}{2}")
    ws.merge_cells("%s%s:%s%s" %(get_column_letter(1),1,get_column_letter(max_wid),2))
    cell = ws["A1"]
    font = Font(name="华文楷体",size=20)
    cell.font = font
    
    ws.cell(row=3, column=1).value = "请验单编号"
    ws.cell(row=3, column=2).value = qydbh
    ws.cell(row=4, column=1).value = "项目编号"
    ws.cell(row=4, column=2).value = xmbh

    ws.cell(row=3, column=half_wid+1).value = "检测编号"
    ws.cell(row=4, column=half_wid+1).value = "检测项目"
    ws.cell(row=3, column=half_wid+2).value = jcbh
    ws.cell(row=4, column=half_wid+2).value = jcxm

    ws.cell(row=5, column=1).value = "检测依据"
    ws.cell(row=5, column=2).value = jcyj
    # ws.merge_cells(f"{get_column_letter(2)}{3}:{get_column_letter(half_wid)}{3}")
    # ws.merge_cells(f"{get_column_letter(2)}{4}:{get_column_letter(half_wid)}{4}")
    # ws.merge_cells(f"{get_column_letter(half_wid+2)}{3}:{get_column_letter(max_wid)}{3}")
    # ws.merge_cells(f"{get_column_letter(half_wid+2)}{4}:{get_column_letter(max_wid)}{4}")
    # ws.merge_cells(f"{get_column_letter(2)}{5}:{get_column_letter(max_wid)}{5}")
    ws.merge_cells("%s%s:%s%s" %(get_column_letter(2),3,get_column_letter(half_wid),3))
    ws.merge_cells("%s%s:%s%s" %(get_column_letter(2),4,get_column_letter(half_wid),4))

    ws.merge_cells("%s%s:%s%s" %(get_column_letter(half_wid+2),3,get_column_letter(max_wid),3))
    ws.merge_cells("%s%s:%s%s" %(get_column_letter(half_wid+2),4,get_column_letter(max_wid),4))
    ws.merge_cells("%s%s:%s%s" %(get_column_letter(2),5,get_column_letter(max_wid),5))

    if checkPlate(dic):
        gap=8

        for plate in dic.keys():
            out=pd.DataFrame(np.zeros([len(info[1]),len(info[2])]), dtype=object)
            out.index=list(map(int,info[1]))
            out.columns=list(map(int,info[2]))
            df=dic[plate]
            for i in range(len(info[1])):
                for j in range(len(info[2])):
                    value=df.loc['1E-'+info[1][i]+'-'+info[2][j],5]
                    out.iloc[i,j]=checkValue(value)
            out=out.sort_index(ascending=False)
            # print(out)
            ws=writeXlsx(wb,ws,out,r=gap,plate=plate)
            gap=gap+len(info[1])+2

    wb.save(out_file)
    return info

def doReport1(input_file,qydbh,xmbh,jcbh,jcxm,jcyj):
    out_f = os.path.split(input_file)
    out_file=out_f[0]+("/Report-"+out_f[1][:-4]+".xlsx")
    file=readFile(u"%s" %input_file)
    dic=getGroup(file)

    info=reportXlsx(dic,out_file=out_file,qydbh=qydbh,xmbh=xmbh,jcbh=jcbh,jcxm=jcxm,jcyj=jcyj)
    out_string=''
    out_string+="Number of Plate: %s <br />" % info[0]
    out_string+="Number of Sample(1E-x): %s; detail: %s  <br />" %(len(info[1]),info[1])
    out_string+="Number of Well: %s  <br />" % len(info[2])
    print(out_string)
    return out_string

