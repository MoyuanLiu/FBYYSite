from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PermissionManage.models import *
from PermissionManage.Form.Forms import *
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from PermissionManage.Logic.permission_controller import *
from UserManage.Logic.usermanage_controller import get_all_departments
import json

# Create your views here.
@csrf_exempt
def rolemanage(request,pagenum):
    rolelist = TbRole.objects.all()
    paginator = Paginator(rolelist, 5)
    totalpages = paginator.num_pages
    queryform = RoleQueryForm()
    currentpage = pagenum
    modules = get_all_modules()
    try:
        rolelist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        rolelist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        rolelist = paginator.page(currentpage)
    rolelist = role_list(rolelist)
    return render(request, "role_manage.html", locals())

@csrf_exempt
def permission_ajax_function(request):
    if request.method == 'GET':
        modulecode = request.GET.get('module_code', None)
        if modulecode:
            data = permission_function_by_module(modulecode)
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)


@csrf_exempt
def roleadd(request):
    modules = get_all_modules()
    if request.method == 'GET':
        form = RoleAddForm()
        return render(request, "role_add.html", locals())
    elif request.method == 'POST':
        form = RoleAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            role_add(cd)
            return redirect("fbyysite/rolemanage/pagenum/1")
        else:
            return render(request, 'role_add.html', locals())

@csrf_exempt
def roleedit(request,roleid):
    role = get_role_by_id(roleid)
    modules = get_all_modules()
    functionlist = get_all_functions()
    refererurl = request.META.get('HTTP_REFERER')
    return render(request, "role_edit.html", locals())

@csrf_exempt
def roleeditcheck(request):
    if request.method == 'POST':
        form = RoleEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            update_role_edit(cd)
            return redirect(request.POST.get('refererurl'))
        else:
            role = get_role_by_id(request.POST.get('roleid'))
            modules = get_all_modules()
            functionlist = get_all_functions()
            refererurl = request.POST.get('refererurl')
            return render(request, 'role_edit.html', locals())

@csrf_exempt
def roledefault(request):
    if request.method == 'POST':
        default_role(request.POST.get('defaultroleid'))
        return redirect(request.POST.get('defaultreferer'))

@csrf_exempt
def roledelete(request):
    if request.method == 'POST':
        delete_role(request.POST.get('delroleid'))
        return redirect(request.POST.get('delreferer'))

@csrf_exempt
def rolequery(request,pagenum):
    if request.method == 'POST':
        queryform = RoleQueryForm(request.POST)
        modules = get_all_modules()
        if queryform.is_valid():
            cd = queryform.cleaned_data
            rolelist = role_query(cd)
            paginator = Paginator(rolelist, 5)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                rolelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                rolelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                rolelist = paginator.page(currentpage)
            rolelist = role_list(rolelist)
            return render(request,'role_query.html',locals())
        else:
            return render(request,'role_query.html',locals())

@csrf_exempt
def permissionmanage(request,pagenum):
    userlist = get_all_users()
    paginator = Paginator(userlist, 8)
    totalpages = paginator.num_pages
    queryform = PermissionQueryForm()
    currentpage = pagenum
    departments = get_all_departments()
    modules = get_all_modules()
    types = get_all_permissiontypes()
    roles = get_all_roles()
    try:
        userlist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        userlist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        userlist = paginator.page(currentpage)
    userlist = user_role_list(userlist)
    return render(request, "permission_manage.html", locals())

@csrf_exempt
def assignpermission(request,userid):
    user = get_user_role_permission_info(userid)
    roles = get_all_roles()
    types = get_all_permissiontypes()
    departments = get_all_departments()
    stores = get_all_stores()
    refererurl = request.META.get('HTTP_REFERER')
    try:
        userroleobj = TbUserRole.objects.get_user_role_by_user_id(userid)
        userrole = get_role_by_id(userroleobj.tb_user_role_roleid)
        permissionlist = get_user_role_permission_list(userid)
        return render(request, "permission_edit.html", locals())
    except:
        return render(request, "permission_edit.html", locals())

@csrf_exempt
def role_ajax_function(request):
    if request.method == 'GET':
        roleid = request.GET.get('role_id', None)
        if roleid:
            data = get_fucnctinlist_by_role_id(roleid)
            result = serializers.serialize('json', data)
            return JsonResponse(result, safe=False)


@csrf_exempt
def permissioneditcheck(request):
    if request.method == 'POST':
        form = PermissionEsitForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            update_permission_edit(cd)
            return redirect(request.POST.get('refererurl'))
        else:
            userid = request.POST.get('userid')
            user = get_user_role_permission_info(userid)
            roles = get_all_roles()
            types = get_all_permissiontypes()
            departments = get_all_departments()
            stores = get_all_stores()
            userrole = get_role_by_id(TbUserRole.objects.get_user_role_by_user_id(userid).tb_user_role_roleid)
            permissionlist = get_user_role_permission_list(userid)
            refererurl = request.POST.get('refererurl')
            return render(request, 'permission_edit.html', locals())

@csrf_exempt
def user_ajax_permission(request):
    if request.method == 'GET':
        userid = request.GET.get('userid', None)
        if userid:
            data = get_user_role_permission_list(userid)
            result = json.dumps(data, ensure_ascii=False)
            return JsonResponse(result, safe=False)


@csrf_exempt
def permissiondelete(request):
    if request.method == 'POST':
        delete_permission(request.POST.get('deluserid'))
        return redirect(request.POST.get('delreferer'))

@csrf_exempt
def querypermission(request,pagenum):
    if request.method == 'POST':
        queryform = PermissionQueryForm(request.POST)
        departments = get_all_departments()
        stores = get_all_stores()
        types = get_all_permissiontypes()
        roles = get_all_roles()
        if queryform.is_valid():
            cd = queryform.cleaned_data
            userlist = permission_query(cd)
            paginator = Paginator(userlist, 8)
            totalpages = paginator.num_pages
            currentpage = pagenum
            try:
                rolelist = paginator.page(currentpage)
            except PageNotAnInteger:
                currentpage = 1
                rolelist = paginator.page(currentpage)
            except EmptyPage:
                currentpage = totalpages
                rolelist = paginator.page(currentpage)
            userlist = user_role_list(userlist)
            return render(request, "permission_query.html", locals())
        else:
            return render(request, "permission_query.html", locals())

