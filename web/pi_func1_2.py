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
    k=[]
    dic={}
    df=[]
    for line in file:
        if line.startswith(group_name):
            count=count+1
            df=[]
        elif line.startswith("Sample"):
            header=line.strip().split('\t')
            k=header
        elif line.startswith("\t")==False and k==['Sample', 'Well', 'Dilution Factor', 'Value', 'Result pg/mL', 'Adj Result pg/mL']:
            y=line.strip().split('\t')
            df.append(y)
        elif line.startswith("\t")==True and count!=0 and k==['Sample', 'Well', 'Dilution Factor', 'Value', 'Result pg/mL', 'Adj Result pg/mL']:
            out=pd.DataFrame(df)
            out.index=out[0]
            dic[count]=out
            k=[]
    # A file may end immediately after the last data row.
    if count!=0 and df and k==['Sample', 'Well', 'Dilution Factor', 'Value', 'Result pg/mL', 'Adj Result pg/mL']:
        out=pd.DataFrame(df)
        out.index=out[0]
        dic[count]=out
    return(dic)

def get_letter_column(letter):
    letter=letter.upper()
    out=0
    d={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10,
       "K":11,"L":12,"M":13,"N":14,"O":15,"P":16,"Q":17,"R":18,"S":19,"T":20,
       "U":21,"V":22,"W":23,"X":24,"Y":25,"Z":26}
    if len(letter)==1:
        out=d[letter]
    else:
        letter=letter[::-1]
        for i in range(len(letter)):
            # print("数字",i)
            # print("字母",letter[i])
            sub_letter=letter[i]
            di=26**i
            # print("底",di)
            # print("数值",di * d[sub_letter])
            sub_value=di * d[sub_letter]
            out=out+sub_value
            
    return out

def switched_letter(x):
    x=int(x)
    d={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10,
       "K":11,"L":12,"M":13,"N":14,"O":15,"P":16,"Q":17,"R":18,"S":19,"T":20,
       "U":21,"V":22,"W":23,"X":24,"Y":25,"Z":26}
    switched_d = {value: key for key, value in d.items()}
    return switched_d[x]

def getPlateInfo(dic,key=1,print_info=False):
    n=len(dic.keys())
    df=dic[key]
    sample=df[0]
    ten_x=[]
    kong=[]
    split_key=""
    sample_key=sample.iloc[0]
    if sample_key.find("-")!=-1:
        split_key="-"
        
        for i in sample:
            line=i.split(split_key)
            ten_x.append(line[1])
            kong.append(line[2])

        k=sorted(list(set(kong)))
        bs=sorted(list(set(ten_x)))
        if(print_info):
            print("Number of Plate:",n)
            print("Number of Sample(10x):",len(bs),"; detail:",bs)
            print("Number of Well",len(k))
        return(n,bs,k)
    
    else:
        for i in sample:
            line=sample[i]
            ten_x.append(get_letter_column(line[:1]))
            kong.append(int(line[1:]))

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
    out=open(file,'r',encoding="utf-8")
    return(out)

def checkValue(value,low=85.2,high=4261.8):
    if value=='NA':
        return "NA"
    elif value=='Range?':
        return "未检出"
    elif float(value)>high:
        return "超上限"
    elif float(value)<low:
        return "未检出"
    else:
        return value

def writeXlsx(wb,ws,out,r,plate,change_index=False):

    result_pd = out #result为处理之后的数据，可以是pivot_table 处理后的数据，也可以是group by 之后的数据
    # result_pd.columns = result_pd.columns.droplevel(0)  # 表头数据转化
    result_pd = result_pd.reset_index()  # 转化index
    col=list(result_pd.columns)
    if change_index:
        col[0]="浓度"
        result_pd.columns=col
        result_pd['浓度']=["(1E-"+str(i)+")" for i in list(result_pd['浓度'])]
        columns = result_pd.columns.values #结果数据的表头
    else:
        col[0]="Row"
        result_pd.columns=col
        result_pd['Row']=[get_column_letter(i) for i in list(result_pd['Row'])]
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
            ws.cell(row=r-1-len(result_pd[3]), column=col).value = columns[col-1] #写入表头
    
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
    for i in range(2, ws.max_row+1):
        ws.row_dimensions[i].height = height
    for i in range(1, ws.max_column+1):
        ws.column_dimensions[get_column_letter(i)].width = width

    return ws
    
def reportXlsx(dic,out_file="out.xlsx",
               qydbh="",xmbh="",jcbh="",jcxm="",jcyj="",check_plate=False):
    info=getPlateInfo(dic,key=1,print_info=True)
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
								
    if check_plate:
        checkPlate(dic)

    gap=8
    for plate in dic.keys():
        info=getPlateInfo(dic,key=plate,print_info=False)

        out=pd.DataFrame(np.zeros([len(info[1]),len(info[2])]), dtype=object)
        out.index=list(map(int,info[1]))
        out.columns=list(map(int,info[2]))
        df=dic[plate]
        if df.index[1].find('1E-')!=-1:
            for i in range(len(info[1])):
                for j in range(len(info[2])):
                    value=df.loc['1E-'+info[1][i]+'-'+info[2][j],5]
                    out.iloc[i,j]=checkValue(value)

        else: #更新
             for i in range(len(info[1])):
                for j in range(len(info[2])):
                    index=get_column_letter(info[1][i])
                    if len(str(info[2][j]))==1:
                        index=index+"0"+str(info[2][j])
                    else:
                        index=index+str(info[2][j])
                    
                    try:
                        value=df.loc[index,5]
                    except:
                        value="NA"
                    # print(index,value)
                    out.iloc[i,j]=checkValue(value)
                    
        if df.index[1].find('1E-')!=-1:
            out=out.sort_index(ascending=False)
        # print(out)
        ws=writeXlsx(wb,ws,out,r=gap,plate=plate)
        gap=gap+len(info[1])+2

    wb.save(out_file)
    return info

def doReport2(input_file,qydbh,xmbh,jcbh,jcxm,jcyj):
    out_f = os.path.split(input_file)
    out_file=out_f[0]+("/Report-"+out_f[1][:-4]+".xlsx")
    file=readFile(u"%s" %input_file)
    dic=getGroup(file)

    info=reportXlsx(dic,out_file=out_file,qydbh=qydbh,xmbh=xmbh,jcbh=jcbh,jcxm=jcxm,jcyj=jcyj)
    hole=[switched_letter(i) for i in info[1]]
    
    out_string=''
    out_string+="Number of Plate: %s <br />" % info[0]
    out_string+="Number of Sample: %s; detail: %s  <br />" %(len(info[1]),hole)
    out_string+="Number of Well: %s  <br />" % len(info[2])
    print(out_string)
    return out_string
    
