from django.shortcuts import render,redirect
from SiteLogin.Logic.login_controller import *
from SiteLogin.Logic.registe_controller import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
import logging
from django.core import serializers
from SiteLogin.Form.Forms import *
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def login(request):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        a = request.POST.get('email','')
        logger.info("account is %s" %a)
        p = request.POST.get('pwd','')
        rem = request.POST.get('pwd','')
        if logincheck(a,p,rem):
            request.session['usenname'] = a
            currentdatetime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            login_update(a,currentdatetime)
            return HttpResponseRedirect('/fbyysite/index/')
        else:
            return render(request, "login.html")
    else:
        return render(request, "login.html")

@csrf_exempt
def registe(request):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    departmentlist = registe_departments()
    if request.method == 'GET':
        form = RegisteForm()
        return render(request,"registe.html",{'departments':departmentlist,'stores':{},'form':form})
    elif request.method == 'POST':
        form = RegisteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            active_tocken = uuid.uuid1()
            msg = '本邮件为系统用户激活邮件，如非本人操作，请忽略。<a href="http://%s/fbyysite/active/%s" target="_blank">点击激活</a>激活链接将在60秒后失效！！' %(request.get_host(),active_tocken)
            emaillist = []
            emaillist.append(cd['email'])

            send_mail('注册激活邮件','以下是用户激活邮件，如非本人操作，请忽略。',settings.DEFAULT_FROM_EMAIL,emaillist,fail_silently=False,html_message=msg)
            cache.set(active_tocken, cd, 60)
            msgpre = '已发送激活邮件请查收'
            seconds = 3
            msgsuf = '秒后关闭'
            metacontent = "%s" % (seconds)
            return render(request, 'jumpclose.html',
                          {'msgpre': msgpre, 'seconds': seconds, 'msgsuf': msgsuf,'metacontent': metacontent})
        else:
            return render(request,'registe.html', {'departments':departmentlist,'stores':{},'form': form})

@csrf_exempt
def registe_ajax_store(request):
    if request.method == 'GET':
        departcode = request.GET.get('depart_code', None)
        if departcode:
            data = registe_store_by_department(departcode)
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)

@csrf_exempt
def index(request):
    username = request.session.get('usenname')
    if user_permission_check(username):
        return render(request, "index.html",{'rolename':'超级管理员'})
    else:
        rolename = get_user_role_name(username)
        return render(request, "index.html", {'rolename': rolename})


@csrf_exempt
def about(request):
    return render(request,"about.html")

@csrf_exempt
def requires_login(view):
    def new_view(request, *args, **kwargs):
        username = request.session.get('usenname')
        if not isauthenticated(username):
            return HttpResponseRedirect('/fbyysite/login')
        return view(request, *args, **kwargs)
    return new_view

@csrf_exempt
def activeaccount(request,tocken):
    if cache.get(tocken) == None:
        return redirect('/fbyysite/jump/fail')
    else:
        formdata = cache.get(tocken)
        registe_active_account(formdata)
        return redirect('/fbyysite/jump/success')

@csrf_exempt
def tmpjump(request,flag):
    if flag=='fail':
        msgpre = '链接已失效'
        seconds = 3
        msgsuf = '秒后跳转至注册页面'
        redirecturl = '/fbyysite/registe'
        metacontent = "%s;URL=%s"%(seconds,redirecturl)
        return render(request,'jump.html',{'msgpre': msgpre, 'seconds': seconds, 'msgsuf': msgsuf, 'redirecturl': redirecturl,'metacontent':metacontent})
    elif flag == 'success':
        msgpre = '用户已激活'
        seconds = 3
        msgsuf = '秒后跳转至登录页面'
        redirecturl = '/fbyysite/login'
        metacontent = "%s;URL=%s" % (seconds, redirecturl)
        return render(request, 'jump.html',{'msgpre': msgpre, 'seconds': seconds, 'msgsuf': msgsuf, 'redirecturl': redirecturl,'metacontent':metacontent})

@csrf_exempt
def index_left(request):
    username = request.session.get('usenname')
    if user_permission_check(username):
        modulelist = get_all_modules()
        functionlist = get_all_functions()
        return render(request, "index_left.html", {'modules': modulelist,'functions':functionlist})
    else:
        modulelist = get_user_modules(username)
        functionlist = get_user_functions(username)
        return render(request, "index_left.html", {'modules': modulelist,'functions':functionlist})


@csrf_exempt
def index_content(request):
    return render(request, "index_content.html")

@csrf_exempt
def logout(request):
    cache.delete(request.session.get('usenname'),None)
    #print(request.session.get('usenname'))
    cursessionkey = request.session.session_key
    request.session.delete(cursessionkey)
    return redirect('/fbyysite/index/')




