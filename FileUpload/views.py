# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime

# Create your views here.
def upload(request):
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None
        File = request.FILES.get("tempfile", None)
        if File is None:
            return HttpResponse("没有需要上传的文件")
        else:
            # 打开特定的文件进行二进制的写操作
            # print(os.path.exists('/temp_file/'))
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with open("../FileUpload/temp_file/%s" % (currenttimestamp +"." + filenamepart[-1]), 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)
            return HttpResponse("UPload over!")
    return render(request,'file_upload.html')