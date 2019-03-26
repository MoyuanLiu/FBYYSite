# -*- coding: UTF-8 -*-
from django.shortcuts import render,redirect
from DataManage.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from DataManage.Form.Forms import *
from django.views.decorators.csrf import csrf_exempt
from DataManage.Logic.productmanage_controller import *
from DataManage.Logic.ordermanage_controller import *
from DataManage.Logic.storagemanage_controller import *
from DataManage.Logic.ztcmanage_controller import *
from DataManage.Logic.storemanage_controller import *
from django.http import HttpResponse
from django.http import JsonResponse
from FBYYSite.settings import BASE_DIR
import os

# Create your views here.

@csrf_exempt
def ztcmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'ztcmanage', 'query')
    editpermission = get_permission_by_account(account, 'ztcmanage', 'edit')
    delpermission = get_permission_by_account(account, 'ztcmanage', 'del')
    uploadpermission = get_permission_by_account(account, 'ztcmanage', 'upload')
    ztclist = get_ztc_data_by_permission(querypermission)
    paginator = Paginator(ztclist, 8)
    totalpages = paginator.num_pages
    queryform = ZTCQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        ztclist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        ztclist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        ztclist = paginator.page(currentpage)
    return render(request, 'ztc_manage.html', locals())

@csrf_exempt
def ztcquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'ztcmanage', 'query')
        departments = querypermission['departlist']
        queryform = ZTCQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'ztcmanage', 'edit')
        delpermission = get_permission_by_account(account, 'ztcmanage', 'del')
        editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
        delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            cd['ztcsearchtype'] = request.POST.getlist('ztcsearchtype')
            cd['ztctrafficsouce'] = request.POST.getlist('ztctrafficsouce')
            ztclist = ztc_query(cd)
            paginator = Paginator(ztclist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                ztclist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                ztclist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                ztclist = paginator.page(currentpage)
            return render(request,'ztc_query.html',locals())
        else:
            departments = querypermission['departlist']
            ztclist = get_ztc_data_by_permission(querypermission)
            paginator = Paginator(ztclist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                ztclist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                ztclist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                ztclist = paginator.page(currentpage)
            return render(request, 'ztc_query.html', locals())


@csrf_exempt
def ztcupload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            File = request.FILES['uploadFile']
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            uploaddepart = request.POST.get('uploadztcdepart')
            uploadstore = request.POST.get('uploadztcstore')
            filesavepath = os.path.join(BASE_DIR,('TmpFile\\ZTC\\Upload\\'+uploaddepart+'-'+uploadstore+'-'+currenttimestamp +"." + filenamepart[-1]))
            uploadflag = handle_uploaded_file(File,filesavepath)
            if uploadflag:
                account = request.session['usenname']
                taskcontent = dict()
                taskcontent['savepath'] = filesavepath
                taskcontent['savepathname'] = uploaddepart+'-'+uploadstore+'-'+currenttimestamp +"." + filenamepart[-1]
                taskcontent['fileuploadname'] = File.name.encode('utf-8').decode("utf-8")
                createztcimporttask(account,taskcontent)
                return render(request,'upload_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'upload_result.html', {'alertmsg': 'fail'})
        else:
            return render(request,'upload_result.html',{'alertmsg':'warning'})

@csrf_exempt
def ztc_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            querypermission = get_permission_by_account(account, 'ztcmanage', 'query')
            data = get_store_by_department(departcode,querypermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)


@csrf_exempt
def ztc_upload_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            uploadpermission = get_permission_by_account(account, 'ztcmanage', 'upload')
            data = get_store_by_department(departcode,uploadpermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)


@csrf_exempt
def ztcuploadtaskquery(request,pagenum):
    tasknamelist = []
    tasknamelist.append('直通车数据上传导入任务')
    cururl = '/fbyysite/datamanage/ztc/upload/taskquery/1'
    lastlevelurl = '/fbyysite/datamanage/ztc/pagenum/1'
    if request.method == "POST":
        queryform=UploadTaskQueryForm(request.POST)
        if queryform.is_valid():
            account = request.session['usenname']
            cd = queryform.cleaned_data
            tasklist = task_query(account,tasknamelist,'上传',cd)
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
            tasklist = task_query_only_by_user(account, tasknamelist, '上传')
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
        queryform = UploadTaskQueryForm()
        tasklist = task_query_only_by_user(account,tasknamelist,'上传')
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
def productmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account,'productmanage','query')
    editpermission = get_permission_by_account(account,'productmanage','edit')
    delpermission = get_permission_by_account(account,'productmanage','del')
    uploadpermission = get_permission_by_account(account,'productmanage','upload')
    productlist = get_product_data_by_permission(querypermission)
    paginator = Paginator(productlist, 8)
    totalpages = paginator.num_pages
    queryform = ProductQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
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
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'productmanage', 'query')
        departments = querypermission['departlist']
        queryform = ProductQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'productmanage', 'edit')
        delpermission = get_permission_by_account(account, 'productmanage', 'del')
        editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
        delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
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
            departments = querypermission['departlist']
            productlist = get_product_data_by_permission(querypermission)
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
            return render(request, 'product_query.html', locals())

@csrf_exempt
def productupload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            File = request.FILES['uploadFile']
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            uploaddepart = request.POST.get('uploadproductdepart')
            uploadstore = request.POST.get('uploadproductstore')
            filesavepath = os.path.join(BASE_DIR,('TmpFile\\Product\\Upload\\'+uploaddepart+'-'+uploadstore+'-'+currenttimestamp +"." + filenamepart[-1]))
            uploadflag = handle_uploaded_file(File,filesavepath)
            if uploadflag:
                account = request.session['usenname']
                taskcontent = dict()
                taskcontent['savepath'] = filesavepath
                taskcontent['savepathname'] = uploaddepart+'-'+uploadstore+'-'+currenttimestamp +"." + filenamepart[-1]
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
    tasknamelist = []
    tasknamelist.append('商品数据上传导入任务')
    cururl = '/fbyysite/datamanage/product/upload/taskquery/1'
    lastlevelurl = '/fbyysite/datamanage/product/pagenum/1'
    if request.method == "POST":
        queryform=UploadTaskQueryForm(request.POST)
        if queryform.is_valid():
            account = request.session['usenname']
            cd = queryform.cleaned_data
            tasklist = task_query(account,tasknamelist,'上传',cd)
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
            tasklist = task_query_only_by_user(account, tasknamelist, '上传')
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
        queryform = UploadTaskQueryForm()
        tasklist = task_query_only_by_user(account,tasknamelist,'上传')
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
def taskcancel(request):
    if request.method == "POST":
        taskid = request.POST.get('canceltaskid')
        refererurl = request.POST.get('canceltaskreferer')
        if cancel_task_check(taskid):
            cancel_task_by_taskid(taskid)
            return redirect(refererurl,locals())
        else:
            cancelerr=True
            return redirect(refererurl, locals())

@csrf_exempt
def product_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            querypermission = get_permission_by_account(account, 'productmanage', 'query')
            data = get_store_by_department(departcode,querypermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)

@csrf_exempt
def product_upload_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            uploadpermission = get_permission_by_account(account, 'productmanage', 'upload')
            data = get_store_by_department(departcode,uploadpermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)


@csrf_exempt
def ordermanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'ordermanage', 'query')
    editpermission = get_permission_by_account(account, 'ordermanage', 'edit')
    delpermission = get_permission_by_account(account, 'ordermanage', 'del')
    uploadpermission = get_permission_by_account(account, 'ordermanage', 'upload')
    orderlist = get_order_data_by_permission(querypermission)
    paginator = Paginator(orderlist, 8)
    totalpages = paginator.num_pages
    queryform = OrderQueryForm()
    uploadform = FileUploadForm()
    uploadclickfirmform = ClickFirmFileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        orderlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        orderlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        orderlist = paginator.page(currentpage)
    return render(request, 'order_manage.html', locals())

@csrf_exempt
def orderquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'ordermanage', 'query')
        departments = querypermission['departlist']
        queryform = OrderQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'ordermanage', 'edit')
        delpermission = get_permission_by_account(account, 'ordermanage', 'del')
        editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
        delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            orderlist = order_query(cd)
            paginator = Paginator(orderlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                orderlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                orderlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                orderlist = paginator.page(currentpage)
            return render(request,'order_query.html',locals())
        else:
            departments = querypermission['departlist']
            orderlist = get_order_data_by_permission(querypermission)
            paginator = Paginator(orderlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                orderlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                orderlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                orderlist = paginator.page(currentpage)
            return render(request, 'order_query.html', locals())

@csrf_exempt
def order_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            querypermission = get_permission_by_account(account, 'ordermanage', 'query')
            data = get_store_by_department(departcode,querypermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)


@csrf_exempt
def order_upload_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            uploadpermission = get_permission_by_account(account, 'productmanage', 'upload')
            data = get_store_by_department(departcode,uploadpermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)

@csrf_exempt
def orderupload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            File = request.FILES['uploadFile']
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            uploaddepart = request.POST.get('uploadorderdepart')

            filesavepath = os.path.join(BASE_DIR,('TmpFile\\Order\\Upload\\'+uploaddepart+'-'+currenttimestamp +"." + filenamepart[-1]))
            uploadflag = handle_uploaded_file(File,filesavepath)
            if uploadflag:
                account = request.session['usenname']
                taskcontent = dict()
                taskcontent['savepath'] = filesavepath
                taskcontent['savepathname'] = uploaddepart+'-'+currenttimestamp +"." + filenamepart[-1]
                taskcontent['fileuploadname'] = File.name.encode('utf-8').decode("utf-8")
                createorderimporttask(account,taskcontent)
                return render(request,'upload_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'upload_result.html', {'alertmsg': 'fail'})
        else:
            return render(request,'upload_result.html',{'alertmsg':'warning'})

@csrf_exempt
def orderclickfirmupload(request):
    if request.method == "POST":
        form = ClickFirmFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            File = request.FILES['uploadclickfirmFile']
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            uploaddepart = request.POST.get('uploadorderclickfirmdepart')
            filesavepath = os.path.join(BASE_DIR,('TmpFile\\OrderClickFirm\\Upload\\'+uploaddepart+'-'+currenttimestamp +"." + filenamepart[-1]))
            uploadflag = handle_uploaded_file(File,filesavepath)
            if uploadflag:
                account = request.session['usenname']
                taskcontent = dict()
                taskcontent['savepath'] = filesavepath
                taskcontent['savepathname'] = uploaddepart+'-'+currenttimestamp +"." + filenamepart[-1]
                taskcontent['fileuploadname'] = File.name.encode('utf-8').decode("utf-8")
                createorderclickfirmimporttask(account,taskcontent)
                return render(request,'upload_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'upload_result.html', {'alertmsg': 'fail'})
        else:
            return render(request,'upload_result.html',{'alertmsg':'warning'})

@csrf_exempt
def orderuploadtaskquery(request,pagenum):
    tasknamelist = []
    tasknamelist.append('万里牛订单数据上传导入任务')
    tasknamelist.append('万里牛刷单数据上传导入任务')
    cururl = '/fbyysite/datamanage/order/upload/taskquery/1'
    lastlevelurl = '/fbyysite/datamanage/order/pagenum/1'
    if request.method == "POST":
        queryform=UploadTaskQueryForm(request.POST)
        if queryform.is_valid():
            account = request.session['usenname']
            cd = queryform.cleaned_data
            tasklist = task_query(account,tasknamelist,'上传',cd)
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
            tasklist = task_query_only_by_user(account, tasknamelist, '上传')
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
        queryform = UploadTaskQueryForm()
        tasklist = task_query_only_by_user(account,tasknamelist,'上传')
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
def storagemanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storagemanage', 'query')
    editpermission = get_permission_by_account(account, 'storagemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storagemanage', 'del')
    uploadpermission = get_permission_by_account(account, 'storagemanage', 'upload')
    storagelist = get_storage_data_by_permission(querypermission)
    paginator = Paginator(storagelist, 8)
    totalpages = paginator.num_pages
    queryform = StorageQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
    delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
    try:
        storagelist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storagelist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storagelist = paginator.page(currentpage)
    return render(request, 'storage_manage.html', locals())

@csrf_exempt
def storagequery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storagemanage', 'query')
        departments = querypermission['departlist']
        queryform = StorageQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storagemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storagemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storagelist = storage_query(cd)
            paginator = Paginator(storagelist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storagelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storagelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storagelist = paginator.page(currentpage)
            return render(request,'storage_query.html',locals())
        else:
            departments = querypermission['departlist']
            storagelist = get_order_data_by_permission(querypermission)
            paginator = Paginator(storagelist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storagelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storagelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storagelist = paginator.page(currentpage)
            return render(request, 'storage_query.html', locals())

@csrf_exempt
def storageupload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            File = request.FILES['uploadFile']
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            uploaddepart = request.POST.get('uploadstoragedepart')
            filesavepath = os.path.join(BASE_DIR,('TmpFile\\Storage\\Upload\\'+uploaddepart+'-'+currenttimestamp +"." + filenamepart[-1]))
            uploadflag = handle_uploaded_file(File,filesavepath)
            if uploadflag:
                account = request.session['usenname']
                taskcontent = dict()
                taskcontent['savepath'] = filesavepath
                taskcontent['savepathname'] = uploaddepart+'-'+currenttimestamp +"." + filenamepart[-1]
                taskcontent['fileuploadname'] = File.name.encode('utf-8').decode("utf-8")
                createstorageimporttask(account,taskcontent)
                return render(request,'upload_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'upload_result.html', {'alertmsg': 'fail'})
        else:
            return render(request,'upload_result.html',{'alertmsg':'warning'})

@csrf_exempt
def storageuploadtaskquery(request,pagenum):
    tasknamelist = []
    tasknamelist.append('万里牛库存数据上传导入任务')
    cururl = '/fbyysite/datamanage/storage/upload/taskquery/1'
    lastlevelurl = '/fbyysite/datamanage/storage/pagenum/1'
    if request.method == "POST":
        queryform=UploadTaskQueryForm(request.POST)
        if queryform.is_valid():
            account = request.session['usenname']
            cd = queryform.cleaned_data
            tasklist = task_query(account,tasknamelist,'上传',cd)
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
            tasklist = task_query(account, tasknamelist, '上传')
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
        queryform = UploadTaskQueryForm()
        tasklist = task_query_only_by_user(account,tasknamelist,'上传')
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
def storemanage(request):
    account = request.session['usenname']
    uploadpermission = get_permission_by_account(account, 'storemanage', 'upload')
    uploadform = FileUploadForm()
    departments = uploadpermission['departlist']
    return render(request, 'store_manage.html', locals())

@csrf_exempt
def store_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            querypermission = get_permission_by_account(account, 'storemanage', 'query')
            data = get_store_by_department(departcode,querypermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)

@csrf_exempt
def store_upload_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            uploadpermission = get_permission_by_account(account, 'storemanage', 'upload')
            data = get_store_by_department(departcode,uploadpermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)

@csrf_exempt
def storeupload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            File = request.FILES['uploadFile']
            filenamepart = File.name.split(".")
            currenttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            uploaddepart = request.POST.get('uploadstoredepart')
            uploadstore = request.POST.get('uploadstorestore')
            filesavepath = os.path.join(BASE_DIR,('TmpFile\\Store\\Upload\\'+uploaddepart+'-'+uploadstore+'-'+currenttimestamp +"." + filenamepart[-1]))
            uploadflag = handle_uploaded_file(File,filesavepath)
            if uploadflag:
                account = request.session['usenname']
                taskcontent = dict()
                taskcontent['savepath'] = filesavepath
                taskcontent['savepathname'] = uploaddepart+'-'+uploadstore+'-'+currenttimestamp +"." + filenamepart[-1]
                taskcontent['fileuploadname'] = File.name.encode('utf-8').decode("utf-8")
                createstoreimporttask(account,taskcontent)
                return render(request,'upload_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'upload_result.html', {'alertmsg': 'fail'})
        else:
            return render(request,'upload_result.html',{'alertmsg':'warning'})


@csrf_exempt
def storecostmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storecostlist = get_store_cost_data_by_permission(querypermission)
    paginator = Paginator(storecostlist, 8)
    totalpages = paginator.num_pages
    queryform = StoreCostQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storecostlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storecostlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storecostlist = paginator.page(currentpage)
    return render(request, 'storecost_manage.html', locals())

@csrf_exempt
def storecostquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreCostQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storecostlist = storecost_query(cd)
            paginator = Paginator(storecostlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storecostlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storecostlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storecostlist = paginator.page(currentpage)
            return render(request,'storecost_query.html',locals())
        else:
            departments = querypermission['departlist']
            storecostlist = get_store_cost_data_by_permission(querypermission)
            paginator = Paginator(storecostlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storecostlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storecostlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storecostlist = paginator.page(currentpage)
            return render(request, 'storecost_query.html', locals())

@csrf_exempt
def storeflowmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storeflowlist = get_store_flow_data_by_permission(querypermission)
    paginator = Paginator(storeflowlist, 8)
    totalpages = paginator.num_pages
    queryform = StoreFlowQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storeflowlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storeflowlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storeflowlist = paginator.page(currentpage)
    return render(request, 'storeflow_manage.html', locals())

def storeflowquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreFlowQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storeflowlist = storeflow_query(cd)
            paginator = Paginator(storeflowlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeflowlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeflowlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeflowlist = paginator.page(currentpage)
            return render(request,'storeflow_query.html',locals())
        else:
            departments = querypermission['departlist']
            storeflowlist = get_store_flow_data_by_permission(querypermission)
            paginator = Paginator(storeflowlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeflowlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeflowlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeflowlist = paginator.page(currentpage)
            return render(request, 'storeflow_query.html', locals())

@csrf_exempt
def storeinteractionmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storeinteractionlist = get_store_interaction_data_by_permission(querypermission)
    paginator = Paginator(storeinteractionlist, 8)
    totalpages = paginator.num_pages
    queryform = StoreInteractionQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storeinteractionlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storeinteractionlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storeinteractionlist = paginator.page(currentpage)
    return render(request, 'storeinteraction_manage.html', locals())

@csrf_exempt
def storeinteractionquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreInteractionQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storeinteractionlist = storeinteraction_query(cd)
            paginator = Paginator(storeinteractionlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeinteractionlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeinteractionlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeinteractionlist = paginator.page(currentpage)
            return render(request,'storeinteraction_query.html',locals())
        else:
            departments = querypermission['departlist']
            storeinteractionlist = get_store_interaction_data_by_permission(querypermission)
            paginator = Paginator(storeinteractionlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeinteractionlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeinteractionlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeinteractionlist = paginator.page(currentpage)
            return render(request, 'storeinteraction_query.html', locals())

@csrf_exempt
def storelogisticmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storelogisticlist = get_store_logistic_data_by_permission(querypermission)
    paginator = Paginator(storelogisticlist, 8)
    totalpages = paginator.num_pages
    queryform = StoreLogisticQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storelogisticlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storelogisticlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storelogisticlist = paginator.page(currentpage)
    return render(request, 'storelogistic_manage.html', locals())

@csrf_exempt
def storelogisticquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreLogisticQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storelogisticlist = storelogistic_query(cd)
            paginator = Paginator(storelogisticlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storelogisticlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storelogisticlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storelogisticlist = paginator.page(currentpage)
            return render(request,'storelogistic_query.html',locals())
        else:
            departments = querypermission['departlist']
            storelogisticlist = get_store_logistic_data_by_permission(querypermission)
            paginator = Paginator(storelogisticlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storelogisticlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storelogisticlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storelogisticlist = paginator.page(currentpage)
            return render(request, 'storelogistic_query.html', locals())

@csrf_exempt
def storereviewmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storereviewlist = get_store_review_data_by_permission(querypermission)
    paginator = Paginator(storereviewlist, 8)
    totalpages = paginator.num_pages
    queryform = StoreReviewQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storereviewlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storereviewlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storereviewlist = paginator.page(currentpage)
    return render(request, 'storereview_manage.html', locals())

@csrf_exempt
def storereviewquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreReviewQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storereviewlist = storereview_query(cd)
            paginator = Paginator(storereviewlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storereviewlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storereviewlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storereviewlist = paginator.page(currentpage)
            return render(request,'storereview_query.html',locals())
        else:
            departments = querypermission['departlist']
            storereviewlist = get_store_review_data_by_permission(querypermission)
            paginator = Paginator(storereviewlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storereviewlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storereviewlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storereviewlist = paginator.page(currentpage)
            return render(request, 'storereview_query.html', locals())

@csrf_exempt
def storeservicemanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storeservicelist = get_store_service_data_by_permission(querypermission)
    paginator = Paginator(storeservicelist, 8)
    totalpages = paginator.num_pages
    queryform = StoreServiceQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storeservicelist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storeservicelist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storeservicelist = paginator.page(currentpage)
    return render(request, 'storeservice_manage.html', locals())

@csrf_exempt
def storeservicequery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreServiceQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storeservicelist = storeservice_query(cd)
            paginator = Paginator(storeservicelist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeservicelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeservicelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeservicelist = paginator.page(currentpage)
            return render(request,'storeservice_query.html',locals())
        else:
            departments = querypermission['departlist']
            storeservicelist = get_store_service_data_by_permission(querypermission)
            paginator = Paginator(storeservicelist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeservicelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeservicelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeservicelist = paginator.page(currentpage)
            return render(request, 'storeservice_query.html', locals())

@csrf_exempt
def storetrademanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storetradelist = get_store_trade_data_by_permission(querypermission)
    paginator = Paginator(storetradelist, 8)
    totalpages = paginator.num_pages
    queryform = StoreTradeQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storetradelist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storetradelist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storetradelist = paginator.page(currentpage)
    return render(request, 'storetrade_manage.html', locals())

@csrf_exempt
def storetradequery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreTradeQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storetradelist = storetrade_query(cd)
            paginator = Paginator(storetradelist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storetradelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storetradelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storetradelist = paginator.page(currentpage)
            return render(request,'storetrade_query.html',locals())
        else:
            departments = querypermission['departlist']
            storetradelist = get_store_trade_data_by_permission(querypermission)
            paginator = Paginator(storetradelist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storetradelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storetradelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storetradelist = paginator.page(currentpage)
            return render(request, 'storetrade_query.html', locals())

@csrf_exempt
def storeturnmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'storemanage', 'query')
    editpermission = get_permission_by_account(account, 'storemanage', 'edit')
    delpermission = get_permission_by_account(account, 'storemanage', 'del')
    storeturnlist = get_store_turn_data_by_permission(querypermission)
    paginator = Paginator(storeturnlist, 8)
    totalpages = paginator.num_pages
    queryform = StoreTurnQueryForm()
    uploadform = FileUploadForm()
    currentpage = pagenum
    departments = querypermission['departlist']
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])
    try:
        storeturnlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        storeturnlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        storeturnlist = paginator.page(currentpage)
    return render(request, 'storeturn_manage.html', locals())

@csrf_exempt
def storeturnquery(request,pagenum):
    if request.method == 'POST':
        account = request.session['usenname']
        querypermission = get_permission_by_account(account, 'storemanage', 'query')
        departments = querypermission['departlist']
        queryform = StoreTurnQueryForm(request.POST)
        editpermission = get_permission_by_account(account, 'storemanage', 'edit')
        delpermission = get_permission_by_account(account, 'storemanage', 'del')
        editpermissiondepartcodelist = get_permission_depart_code_list(editpermission['departlist'])
        delpermissiondepartcodelist = get_permission_depart_code_list(delpermission['departlist'])
        if queryform.is_valid():
            cd = queryform.cleaned_data
            storeturnlist = storeturn_query(cd)
            paginator = Paginator(storeturnlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeturnlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeturnlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeturnlist = paginator.page(currentpage)
            return render(request,'storeturn_query.html',locals())
        else:
            departments = querypermission['departlist']
            storeturnlist = get_store_turn_data_by_permission(querypermission)
            paginator = Paginator(storeturnlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                storeturnlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                storeturnlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                storeturnlist = paginator.page(currentpage)
            return render(request, 'storeturn_query.html', locals())

@csrf_exempt
def storeuploadtaskquery(request,pagenum):
    tasknamelist=[]
    tasknamelist.append('店铺数据上传导入任务')
    cururl = '/fbyysite/datamanage/store/upload/taskquery/1'
    lastlevelurl = '/fbyysite/datamanage/store/'
    if request.method == "POST":
        queryform=UploadTaskQueryForm(request.POST)
        if queryform.is_valid():
            account = request.session['usenname']
            cd = queryform.cleaned_data
            tasklist = task_query(account,tasknamelist,'上传',cd)
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
            tasklist = task_query_only_by_user(account, tasknamelist, '上传')
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
        queryform = UploadTaskQueryForm()
        tasklist = task_query_only_by_user(account, tasknamelist, '上传')
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

