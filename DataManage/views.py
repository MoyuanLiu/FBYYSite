# -*- coding: UTF-8 -*-
from django.shortcuts import render,redirect
from DataManage.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from DataManage.Form.Forms import *
from UserManage.Logic.usermanage_controller import *
from django.views.decorators.csrf import csrf_exempt
from DataManage.Logic.productmanage_controller import *
from django.http import HttpResponse
from FBYYSite.settings import BASE_DIR
import os
# Create your views here.

def ztcmanage(request):
    return

@csrf_exempt
def productmanage(request,pagenum):
    productlist = TbProduct.objects.all()
    paginator = Paginator(productlist, 8)
    totalpages = paginator.num_pages
    queryform = ProductQueryForm()
    uploadform = ProductUploadForm()
    currentpage = pagenum
    departments = get_all_departments()
    try:
        productlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        productlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        productlist = paginator.page(currentpage)
    return render(request,'product_manage.html',locals())

@csrf_exempt
def productquery(request,pagenum):
    if request.method == 'POST':
        departments = get_all_departments()
        queryform = ProductQueryForm(request.POST)
        if queryform.is_valid():
            cd = queryform.cleaned_data
            productlist = product_query(cd)
            paginator = Paginator(productlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                productlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                productlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                productlist = paginator.page(currentpage)
            return render(request,'product_query.html',locals())
        else:
            departments = get_all_departments()
            return render(request,'product_query.html',locals())

@csrf_exempt
def productupload(request):
    if request.method == "POST":
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            File = request.FILES['uploadFile']
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filepathname = os.path.join(BASE_DIR,('TmpFile/Product/Upload/'+currenttimestamp +"." + filenamepart[-1]))
            uploadflag = handle_uploaded_file(File,filepathname)
            if uploadflag:
                account = request.session['usenname']
                taskcontent = dict()
                taskcontent['savepathname'] = filepathname
                taskcontent['fileuploadname'] = File.name.encode('utf-8').decode("utf-8")
                createproductimporttask(account,taskcontent)
                return render(request,'upload_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'upload_result.html', {'alertmsg': 'fail'})
        else:
            return render(request,'upload_result.html',{'alertmsg':'warning'})

def handle_uploaded_file(f,filepathname):
    try:
        with open(filepathname, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except:
        return False


@csrf_exempt
def productuploadtaskquery(request,pagenum):
    if request.method == "POST":
        queryform=ProductUploadTaskQueryForm(request.POST)
        if queryform.is_valid():
            account = request.session['usenname']
            cd = queryform.cleaned_data
            tasklist = producttask_upload_query_by_user(account,'商品数据上传导入任务','上传',cd)
            tasklist = taskuploadfilenamefilter(tasklist, cd['taskuploadfilename'])
            paginator = Paginator(tasklist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                tasklist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                tasklist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                tasklist = paginator.page(currentpage)
            tasklist = getuploadfilenametasklist(tasklist)
            return render(request, 'task_upload_query.html', locals())
        else:
            account = request.session['usenname']
            tasklist = producttask_upload_query_only_by_user(account, '商品数据上传导入任务', '上传')
            paginator = Paginator(tasklist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                tasklist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                tasklist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                tasklist = paginator.page(currentpage)
            tasklist = getuploadfilenametasklist(tasklist)
            return render(request, 'task_upload_manage.html', locals())
    else:
        account = request.session['usenname']
        queryform = ProductUploadTaskQueryForm()
        tasklist = producttask_upload_query_only_by_user(account,'商品数据上传导入任务','上传')
        paginator = Paginator(tasklist, 8)
        totalpages = paginator.num_pages
        currentpage = pagenum
        try:
            tasklist = paginator.page(currentpage)
        except PageNotAnInteger:
            currentpage = 1
            tasklist = paginator.page(currentpage)
        except EmptyPage:
            currentpage = totalpages
            tasklist = paginator.page(currentpage)
        tasklist = getuploadfilenametasklist(tasklist)
        return render(request,'task_upload_manage.html',locals())

@csrf_exempt
def productuploadtaskcancel(request):
    if request.method == "POST":
        taskid = request.POST.get('canceltaskid')
        refererurl = request.POST.get('canceltaskreferer')
        if cancel_product_uploadtask_check(taskid):
            cancel_product_uploadtask_by_taskid(taskid)
            return redirect(refererurl,locals())
        else:
            cancelerr=True
            return redirect(refererurl, locals())


