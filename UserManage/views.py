from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from UserManage.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from UserManage.Form.Forms import *
from UserManage.Logic.usermanage_controller import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from SiteLogin.views import logout

# Create your views here.
@csrf_exempt
def usermanage(request,pagenum):
        userlist = TbUserInfo.objects.all()
        paginator = Paginator(userlist, 8)
        totalpages = paginator.num_pages
        queryform = UserQueryForm()
        currentpage = pagenum
        departments = get_all_departments()
        try:
            userlist = paginator.page(currentpage)
        except PageNotAnInteger:
            currentpage = 1
            userlist = paginator.page(currentpage)
        except EmptyPage:
            currentpage = totalpages
            userlist = paginator.page(currentpage)
        userlist = user_list(userlist)
        return render(request,"user_manage.html",locals())


@csrf_exempt
def useredit(request,account):
    user = TbUserInfo.objects.get_user_by_account(account)
    departmentlist = get_all_departments()
    refererurl = request.META.get('HTTP_REFERER')
    return render(request,"user_edit.html",locals())

@csrf_exempt
def usereditcheck(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            update_user_edit(cd)
            return redirect(request.POST.get('refererurl'))
        else:
            user = TbUserInfo.objects.get_user_by_id(request.POST.get('userid'))
            departmentlist = get_all_departments()
            refererurl = request.POST.get('refererurl')
            return render(request,'user_edit.html', locals())


@csrf_exempt
def userdel(request):
    if request.method == 'POST':
        refererurl = request.POST.get('delreferer')
        user = TbUserInfo.objects.get_user_by_account(request.POST.get('deluseremail'))
        user_del(user.idtb_user_info)
        return redirect(refererurl)


@csrf_exempt
def useradd(request):
    departmentlist = get_all_departments()
    if request.method == 'GET':
        form = UserAddForm()
        return render(request,"user_add.html",locals())
    elif request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_add(cd)
            return redirect("fbyysite/usermanage/pagenum/1")
        else:
            return render(request,'user_add.html', locals())

@csrf_exempt
def userquery(request,pagenum):
    if request.method == 'POST':
        queryform = UserQueryForm(request.POST)
        if queryform.is_valid():
            cd = queryform.cleaned_data
            userlist = user_query(cd)
            paginator = Paginator(userlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                userlist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                userlist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                userlist = paginator.page(currentpage)
            userlist = user_list(userlist)
            return render(request,'user_query.html',locals())
        else:
            return render(request,'user_query.html',locals())

@csrf_exempt
def accountmanage(request):
    if request.method == 'GET':
        account = request.session.get('usenname')
        user = TbUserInfo.objects.get_user_by_account(account)
        departments = get_all_departments()
        return render(request,'account_manage.html',locals())
    else:
        form = AccountEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            update_account_edit(cd)
            return redirect('/fbyysite/accountmanage')
        else:
            user = TbUserInfo.objects.get_user_by_id(request.POST.get('userid'))
            departments = get_all_departments()
            return render(request, 'account_manage.html',locals())

@csrf_exempt
def accountpwdchange(request):
    if request.method == 'POST':
        active_tocken = uuid.uuid1()
        msg = '本邮件为密码修改确认邮件，如非本人操作，请关注本人账号安全。<a href="http://%s/fbyysite/pwdchange/confirm/%s" target="_blank">确认修改密码</a>此链接将在60秒后失效！！' % (
        request.get_host(), active_tocken)
        emaillist = []
        emaillist.append(request.POST.get('resetpwdemail'))

        send_mail('修改密码本人确认邮件', '本邮件为密码修改确认邮件，如非本人操作，请关注本人账号安全。', settings.DEFAULT_FROM_EMAIL, emaillist, fail_silently=False,
                  html_message=msg)
        cache.set(active_tocken, request.POST.get('resetpwdemail'), 60)
        msgpre = '已发送改密确认邮件请查收'
        seconds = 3
        msgsuf = '秒后,跳转回用户中心'
        redirecturl = '/fbyysite/accountmanage'
        metacontent = "%s;URL=%s" % (seconds, redirecturl)
        return render(request, 'jump.html',{'msgpre': msgpre, 'seconds': seconds, 'msgsuf': msgsuf, 'metacontent': metacontent, 'redirecturl': redirecturl})


@csrf_exempt
def accountpwdchangeconfirm(request,tocken):
    if cache.get(tocken) == None:
        msgpre = '链接已失效'
        seconds = 3
        msgsuf = '秒后跳转回用户中心'
        redirecturl = '/fbyysite/accountmanage'
        metacontent = "%s;URL=%s" % (seconds, redirecturl)
        return render(request, 'jump.html',
                      {'msgpre': msgpre, 'seconds': seconds, 'msgsuf': msgsuf, 'redirecturl': redirecturl,
                       'metacontent': metacontent})
    else:
        accountemail = cache.get(tocken)
        return render(request, 'pwd_change.html',{'accountemail',accountemail})


@csrf_exempt
def accountpwdnew(request):
    if request.method == 'POST':
        form = PwdChangeForm(request.Post)
        if form.is_valid():
            cd = form.cleaned_data
            renew_user_pwd(cd)
            logout(request)


@csrf_exempt
def accountemailchange(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if eamil_change_check(cd):
                active_tocken = uuid.uuid1()
                msg = '本邮件为密保邮箱更换确认邮件，如非本人操作，请忽略。<a href="http://%s/fbyysite/emailchange/confirm/%s" target="_blank">激活当前邮箱</a>此链接将在60秒后失效！！' % (
                    request.get_host(), active_tocken)
                emaillist = []
                emaillist.append(cd['email'])
                send_mail('更换本人确认邮件', '本邮件为邮箱更换确认邮件，如非本人操作，请忽略。', settings.DEFAULT_FROM_EMAIL, emaillist,
                          fail_silently=False,
                          html_message=msg)
                cache.set(active_tocken, cd, 60)
                msgpre = '已发送新邮箱激活邮件请查收'
                seconds = 3
                msgsuf = '秒后,跳转回用户中心'
                redirecturl = '/fbyysite/accountmanage'
                metacontent = "%s;URL=%s" % (seconds, redirecturl)
                return render(request, 'jump.html',
                              {'msgpre': msgpre, 'seconds': seconds, 'msgsuf': msgsuf, 'metacontent': metacontent,
                               'redirecturl': redirecturl})
            else:
                logout(request)
        else:
            return render(request,'email_change.html',locals())

@csrf_exempt
def accountemailchangeconfirm(request,tocken):
    if cache.get(tocken) == None:
        msgpre = '链接已失效'
        seconds = 3
        msgsuf = '秒后跳转回用户中心'
        redirecturl = '/fbyysite/accountmanage'
        metacontent = "%s;URL=%s" % (seconds, redirecturl)
        return render(request, 'jump.html',
                      {'msgpre': msgpre, 'seconds': seconds, 'msgsuf': msgsuf, 'redirecturl': redirecturl,
                       'metacontent': metacontent})
    else:
        cd = cache.get(tocken)
        renew_user_eamil(cd)
        return


def renew_user_eamil(formdata):
    user = TbUserInfo.objects.get_user_by_id(formdata['userid'])
    user.tb_user_info_email = formdata['email']
