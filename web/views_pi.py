# -*- coding: utf-8 -*- 
# 脚本用于处理pi-api端上传的文件

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import os

def home(req):
    print("【提示】调用pi-home接口")
    return render(req, 'pi-home.html')

from .pi_func1_2 import doReport2 # 普通
from .pi_func1_1 import doReport1 # 浓度

from django.conf import settings

@csrf_exempt
def func1_result(req):
    print("【提示】调用pi-func1接口")
    if req.method == 'POST':
        File=req.FILES.get("uploadfile", None)
        if File is None:
            return HttpResponse("no files for upload!")
        else:
            # 打开特定的文件进行二进制的写操作;
            try:
                file_name = u"%s" %File.name
                with open(u"%s" %os.path.join(settings.MEDIA_ROOT, file_name), 'wb+') as f:
                    # 分块写入文件;
                    for chunk in File.chunks():
                        f.write(chunk)

            except:
                return HttpResponse("The file name contains illegal characters. <br />Please modify the file name and 'Original Filename' in the file!")
    
            qydbh = req.POST.get("qydbh",'')
            xmbh = req.POST.get("xmbh",'')
            jcbh = req.POST.get("jcbh",'')
            jcxm = req.POST.get("jcxm",'')
            jcyj = req.POST.get("jcyj",'')
            type = req.POST.get("type",'')
            if type=="nd":
                print("【提示】按浓度处理")
                outstring=doReport1(u"%s" %os.path.join(settings.MEDIA_ROOT, file_name),qydbh,xmbh,jcbh,jcxm,jcyj)
            if type=="pd":
                print("【提示】按普通处理")
                outstring=doReport2(u"%s" %os.path.join(settings.MEDIA_ROOT, file_name),qydbh,xmbh,jcbh,jcxm,jcyj)
            outfile="/media/Report-"+file_name[:-4]+".xlsx"
            return HttpResponse("<p>%s 报告描述：</p><p> %s </p><a href='%s'>点击下载结果</a>" %(File.name,outstring,outfile))

