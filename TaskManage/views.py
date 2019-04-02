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
    account = request.session['usenname']
    curuser = get_current_user(account)
    alltasklist = get_task_list_by_user(account)
    paginator = Paginator(alltasklist, 8)
    totalpages = paginator.num_pages
    queryform = AllTaskQueryForm()
    currentpage = pagenum
    users = get_all_users_by_account(account)
    try:
        alltasklist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        alltasklist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        alltasklist = paginator.page(currentpage)
    alltasklist = task_info_list(alltasklist)
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



