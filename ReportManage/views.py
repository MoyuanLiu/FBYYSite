from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ReportManage.models import *
from ReportManage.Form.Forms import *
from UserManage.Logic.usermanage_controller import get_all_departments
from ReportManage.Logic.cts_controller import *
from TaskManage.Logic.taskmanager_controller import get_current_user
from DataManage.Logic.productmanage_controller import get_permission_by_account,get_store_by_department,get_permission_store_code_list
from ReportManage.Logic.kck_controller import *
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@csrf_exempt
def ctsmanage(request,pagenum):
    ctslist = TbCts.objects.all().order_by('-tb_cts_cal_date')
    paginator = Paginator(ctslist, 8)
    totalpages = paginator.num_pages
    queryform = CtsQueryForm()
    makeform = CtsMakeForm()
    currentpage = pagenum
    departments = get_all_departments()
    try:
        ctslist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        ctslist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        ctslist = paginator.page(currentpage)
    return render(request, "cts_manage.html", locals())
@csrf_exempt
def ctsquery(request,pagenum):
    return

@csrf_exempt
def ctsmake(request):
    if request.method == "POST":
        form = CtsMakeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            orderexistsflag=ctsordercheck(cd)
            if orderexistsflag:
                createctsdata(cd)
                return render(request,'make_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'make_result.html', {'alertmsg': 'fail','alertdetail':'没有报表制作所需数据！！！'})
        else:
            return render(request,'make_result.html',{'alertmsg':'warning'})

@csrf_exempt
def kckmanage(request,pagenum):
    account = request.session['usenname']
    querypermission = get_permission_by_account(account, 'kcklistmanage', 'query')
    editpermission = get_permission_by_account(account, 'kcklistmanage', 'edit')
    delpermission = get_permission_by_account(account, 'kcklistmanage', 'del')
    addpermission = get_permission_by_account(account, 'kcklistmanage', 'add')
    departments = querypermission['departlist']
    kcklist = get_kcklist_by_permission(querypermission)
    paginator = Paginator(kcklist, 8)
    totalpages = paginator.num_pages
    queryform = KckQueryForm()
    currentpage = pagenum
    editpermissionstorecodelist = get_permission_store_code_list(editpermission['storelist'])
    delpermissionstorecodelist = get_permission_store_code_list(delpermission['storelist'])

    try:
        kcklist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        kcklist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        kcklist = paginator.page(currentpage)
    kcklist = kck_info_list(kcklist)
    return render(request, "kcklist_manage.html", locals())

@csrf_exempt
def kck_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            account = request.session['usenname']
            querypermission = get_permission_by_account(account, 'kcklistmanage', 'query')
            data = get_store_by_department(departcode,querypermission['storelist'])
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)

@csrf_exempt
def kckadd(request):
    account = request.session['usenname']
    addpermission = get_permission_by_account(account, 'kcklistmanage', 'add')
    departments = addpermission['departlist']
    if request.method == 'GET':
        form = KckAddForm()
        return render(request, "kck_add.html", locals())
    elif request.method == 'POST':
        form = KckAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            kck_add(cd)
            return redirect("fbyysite/reportmanage/kck/pagenum/1")
        else:
            return render(request, 'user_add.html', locals())

@csrf_exempt
def kckedit(request,kckid):
    account = request.session['usenname']
    editpermission = get_permission_by_account(account, 'kcklistmanage', 'edit')
    kck = TbKck.objects.get(idtb_kck=int(kckid))
    departments = editpermission['departlist']
    refererurl = request.META.get('HTTP_REFERER')
    return render(request, "kck_edit.html", locals())

@csrf_exempt
def kckeditcheck(request):
    if request.method == 'POST':
        form = KckEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            update_kck_edit(cd)
            return redirect(request.POST.get('refererurl'))
        else:
            account = request.session['usenname']
            editpermission = get_permission_by_account(account, 'kcklistmanage', 'edit')
            kck = TbKck.objects.get(idtb_kck=request.POST.get('kckid'))
            departments = editpermission['departlist']
            refererurl = request.POST.get('refererurl')
            return render(request,'kck_edit.html', locals())

@csrf_exempt
def kckdel(request):
    if request.method == 'POST':
        refererurl = request.POST.get('delreferer')
        kck = TbKck.objects.get(idtb_kck=int(request.POST.get('delkckid')))
        kck_del(kck.idtb_kck)
        return redirect(refererurl)
