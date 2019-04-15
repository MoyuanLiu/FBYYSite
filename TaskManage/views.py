from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from TaskManage.models import *
from TaskManage.Form.Forms import *
from TaskManage.Logic.taskmanager_controller import *
from multiprocessing import Process
import threading
from threading import Thread
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

threadlist=[]

# Create your views here.
@csrf_exempt
def taskmanage(request,pagenum):
    account = request.session['username']
    curuser = get_current_user(account)
    tasklist = get_task_list_by_user(account)
    paginator = Paginator(tasklist, 8)
    totalpages = paginator.num_pages
    queryform = AllTaskQueryForm()
    currentpage = pagenum
    users = get_all_users_by_account(account)
    userid = curuser.idtb_user_info
    issuperuserflag = curuser.tb_user_info_issuperuser
    try:
        tasklist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        tasklist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        tasklist = paginator.page(currentpage)
    tasklist = task_info_list(tasklist)
    return render(request, "task_manage.html", locals())
@csrf_exempt
def startbgtaskservice(request):
    #p = Process(target=runbackgroundserver)
    logger.info("开启后台进程！！！")
    if threadlist:
        savebgthreadobj = threadlist[-1]
        if savebgthreadobj.isAlive():
            alertmsg = 'warning'
            return render(request, "bgtaskservice_result.html", locals())
        else:
            t = Thread(target=runbackgroundserver)
            try:
                # p.start()
                t.start()
                threadlist.append(t)
                alertmsg = 'success'
                return render(request, "bgtaskservice_result.html", locals())
                bgthreadid = t.ident
                #cache.set('bgthreadobj', t)
            except:
                alertmsg = 'error'
            return render(request, "bgtaskservice_result.html", locals())
    else:
        t = Thread(target=runbackgroundserver)
        try:
            # p.start()
            t.start()
            alertmsg = 'success'
            threadlist.append(t)
            bgthreadid = t.ident
            #cache.set('bgthreadobj', t)
            return render(request, "bgtaskservice_result.html", locals())
        except:
            alertmsg = 'error'
        return render(request, "bgtaskservice_result.html", locals())

@csrf_exempt
def taskquery(request,pagenum):
    if request.method == 'POST':
        queryform = AllTaskQueryForm(request.POST)
        account = request.session['usenname']
        curuser = get_current_user(account)
        users = get_all_users_by_account(account)
        issuperuserflag = curuser.tb_user_info_issuperuser
        if queryform.is_valid():
            cd = queryform.cleaned_data
            tasklist = task_query(cd)
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
            tasklist = task_info_list(tasklist)
            return render(request,'task_query.html',locals())
        else:
            return render(request,'task_query.html',locals())



