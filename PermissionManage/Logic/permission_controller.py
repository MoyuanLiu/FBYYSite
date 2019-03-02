from PermissionManage.models import *
from UserManage.models import TbUserInfo,TbDepartmentInfo,TbStoreInfo
from django.db.models import Q
from UserManage.Logic.usermanage_controller import get_all_departments
from Utils.StringUtil import *
import time

def permission_function_by_module(modulecode):
    functions = TbFunction.objects.get_all_functions_by_module(modulecode)
    return functions

def get_all_modules():
    modules = TbModule.objects.get_all_modules()
    return modules

def role_add(formdata):
    currentdatetime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    TbRole.objects.create_new_role(formdata,currentdatetime)

def get_role_by_id(roleid):
    return TbRole.objects.get(idtb_role=int(roleid))

def update_role_edit(formdata):
    update_role = get_role_by_id(formdata['roleid'])
    update_role.tb_role_code = formdata['rolecode']
    update_role.tb_role_name = formdata['rolename']
    update_role.tb_role_module_list = formdata['selrolemodulelist']
    update_role.tb_role_function_list = formdata['selrolefunctionlist']
    update_role.save()

def get_all_functions():
    functions = TbFunction.objects.ger_all_functions()
    return functions

def role_list(rolelist):
    return TbRole.objects.get_roleinfo_list(rolelist)

def default_role(roleid):
    try:
        lastdefaultrole = TbRole.objects.get(tb_role_default_flag = 1)
        if lastdefaultrole:
            lastdefaultrole.tb_role_default_flag = 0
            lastdefaultrole.save()
        defaultrole = TbRole.objects.get_role_by_id(roleid)
        defaultrole.tb_role_default_flag = 1
        defaultrole.save()
    except:
        defaultrole = TbRole.objects.get_role_by_id(roleid)
        defaultrole.tb_role_default_flag = 1
        defaultrole.save()

def delete_role(roleid):
    delrole = TbRole.objects.get_role_by_id(roleid)
    delrole.delete()

def role_query(formdata):
    condition = Q()
    if formdata['rolecreatedatewhetherflag']:
        condition.children.append(('tb_role_createtime__contains', formdata['rolecreatedate'].strftime('%Y/%m/%d')))
    if formdata['rolecode'] != '' and formdata['rolecode'] != None:
        condition.children.append(('tb_role_code', formdata['rolecode']))
    if formdata['rolename'] != '' and formdata['rolename'] != None:
        condition.children.append(('tb_role_name', formdata['rolename']))
    if formdata['selrolemodule'] != '' and formdata['selrolemodule'] != None:
        condition.children.append(('tb_role_module_list__contains', formdata['selrolemodule']))
    if formdata['selrolefunction'] != '' and formdata['selrolefunction'] != None:
        condition.children.append(('tb_role_function_list__contains', formdata['selrolefunction']))
    if formdata['roledefaultwhetherflag']:
        condition.children.append(('tb_role_default_flag', int(formdata['roledefaultwhether'])))
    query_rolelist = TbRole.objects.filter(condition)
    return query_rolelist

def get_all_users():
    return TbUserInfo.objects.all()

def user_role_list(userlist):
    userrolelist = []
    for user in userlist:
        userroleinfo = {}
        userroleinfo['idtb_user_info'] = user.idtb_user_info
        userroleinfo['tb_user_info_name'] = user.tb_user_info_name
        userroleinfo['tb_user_info_nickname'] = user.tb_user_info_nickname
        userroleinfo['tb_user_info_department_code'] = user.tb_user_info_department_code
        userroleinfo['tb_user_info_department_name'] = TbDepartmentInfo.objects.get_departmentname_by_code(user.tb_user_info_department_code)
        userroleinfo['tb_user_info_store_code'] = user.tb_user_info_store_code
        if user.tb_user_info_store_code == 'Other':
            userroleinfo['tb_user_info_store_name'] = "非店铺"
        else:
            userroleinfo['tb_user_info_store_name'] = TbStoreInfo.objects.get_storecode_by_storecode_by_dapartcode(user.tb_user_info_store_code, user.tb_user_info_department_code)
        userroleinfo['tb_user_info_issuperuser'] = user.tb_user_info_issuperuser
        if user.tb_user_info_issuperuser:
            userroleinfo['tb_user_info_superuser'] = "超级管理员"
        else:
            userroleinfo['tb_user_info_superuser'] = "非超级管理员"
        #userroleinfo['tb_user_permission_range_list'] = TbFunction.objects.get_function_name_list_by_code_list(role.tb_role_function_list)
        try:
            #print('getroleid')
            userroleinfo['tb_user_info_role_id'] = TbUserRole.objects.get_user_role_by_user_id(user.idtb_user_info).tb_user_role_roleid
            role = TbRole.objects.get_role_by_id(userroleinfo['tb_user_info_role_id'])
            userroleinfo['tb_user_info_role_name'] = role.tb_role_name
            userroleinfo['tb_user_info_module_name_list'] = TbModule.objects.get_module_name_list_by_code_list(role.tb_role_module_list)
            userroleinfo['tb_user_info_function_name_list'] = TbFunction.objects.get_function_name_list_by_code_list(role.tb_role_function_list)
            userrolelist.append(userroleinfo)
        except:
            userrolelist.append(userroleinfo)
    return userrolelist

def get_all_permissiontypes():
    return TbPermissionType.objects.all()

def get_user_role_permission_info(userid):
    userrolepermissioninfo = {}
    userrolepermissioninfo['idtb_user_info'] = userid
    user = TbUserInfo.objects.get(idtb_user_info=userid)
    userrolepermissioninfo['tb_user_info_name'] = user.tb_user_info_name
    userrolepermissioninfo['tb_user_info_nickname'] = user.tb_user_info_nickname
    userrolepermissioninfo['tb_user_info_department_name'] = TbDepartmentInfo.objects.get_departmentname_by_code(user.tb_user_info_department_code)
    if user.tb_user_info_store_code == 'Other':
        userrolepermissioninfo['tb_user_info_store_name'] = "非店铺"
    else:
        userrolepermissioninfo['tb_user_info_store_name'] = TbStoreInfo.objects.get_storecode_by_storecode_by_dapartcode(user.tb_user_info_store_code, user.tb_user_info_department_code)
    return userrolepermissioninfo

def get_all_roles():
    return TbRole.objects.all()

def get_all_stores():
    return TbStoreInfo.objects.all()

def get_fucnctinlist_by_role_id(roleid):
    role = TbRole.objects.get(idtb_role=roleid)
    functions = get_all_functions()
    functionlist = []
    for functionitem in functions:
        if functionitem.tb_function_code in role.tb_role_function_list:
            functionlist.append(functionitem)
    return functionlist

def update_user_role(userid,roleid):
    try:
        user_role = TbUserRole.objects.get_user_role_by_user_id(int(userid))
        user_role.tb_user_role_roleid = int(roleid)
        user_role.save()
    except:
        TbUserRole.objects.create(tb_user_role_userid=int(userid),tb_user_role_roleid=int(roleid))


def update_user_permission(updatestr):
    updatestr = updatestr.replace('[','').replace(']','').replace("'",'').replace(" ",'')
    permissionlist = updatestr.split(',')
    for permissioninfo in permissionlist:
        userid = permissioninfo.split('|')[0]
        funccode = permissioninfo.split('|')[1]
        permissiontypecode = permissioninfo.split('|')[2]
        permissionrange = permissioninfo.split('|')[3]
        try:
            urpobj = TbUserRolePermissionManage.objects.get(tb_user_role_permission_manage_user_id=userid,tb_user_role_permission_manage_function_code = funccode,tb_user_role_permission_manage_permission_type_code = permissiontypecode)
            urpobj.tb_user_role_permission_manage_permission_range = permissionrange
            urpobj.save()
        except:
            TbUserRolePermissionManage.objects.create(tb_user_role_permission_manage_user_id=userid,tb_user_role_permission_manage_function_code = funccode,tb_user_role_permission_manage_permission_type_code = permissiontypecode,tb_user_role_permission_manage_permission_range=permissionrange)



def update_permission_edit(formdata):
    update_user_role(formdata['userid'],formdata['selrole'])
    update_user_permission(formdata['selpermission'])

def get_user_role_permission_list(userid):
    permissinlist = []
    try:
        permissinset = TbUserRolePermissionManage.objects.filter(tb_user_role_permission_manage_user_id=userid)
        for permission in permissinset:
            permissioninfo = {}
            permissioninfo['tb_user_role_permission_manage_function_code'] = permission.tb_user_role_permission_manage_function_code
            permissioninfo['tb_user_role_permission_manage_function_name'] = TbFunction.objects.get_function_name_by_code(permission.tb_user_role_permission_manage_function_code)
            permissioninfo['tb_user_role_permission_manage_permission_type_code'] = permission.tb_user_role_permission_manage_permission_type_code
            permissioninfo['tb_user_role_permission_manage_permission_type_name'] = TbPermissionType.objects.get_permission_type_name(permission.tb_user_role_permission_manage_permission_type_code)
            permissioninfo['tb_user_role_permission_manage_permission_range'] = permission.tb_user_role_permission_manage_permission_range
            permissioninfo['permission_info_value_str'] = userid + "|" + permissioninfo['tb_user_role_permission_manage_function_name'] + "|" + permissioninfo['tb_user_role_permission_manage_permission_type_name'] + "|" + permissioninfo['tb_user_role_permission_manage_permission_range']
            permissioninfo['permission_info_text_str'] = userid + "|" + permissioninfo['tb_user_role_permission_manage_function_code'] + "|" + permissioninfo['tb_user_role_permission_manage_permission_type_code'] + "|" + permissioninfo['tb_user_role_permission_manage_permission_range']
            permissinlist.append(permissioninfo)
        return permissinlist
    except:
        return permissinlist

def delete_permission(userid):
    TbUserRole.objects.get_user_role_by_user_id(userid).delete()
    TbUserRolePermissionManage.objects.filter(tb_user_role_permission_manage_user_id=userid).delete()

def permission_query(formdata):
    #retuserlist = []
    user_condition = Q()
    if formdata['querysuperuserwhetherflag']:
        user_condition.children.append(('tb_user_info_issuperuser', int(formdata['querysuperuserwhether'])))
    if formdata['username'] != '' and formdata['username'] != None:
        user_condition.children.append(('tb_user_info_name', formdata['username']))
    if formdata['usernickname'] != '' and formdata['usernickname'] != None:
        user_condition.children.append(('tb_user_info_nickname', formdata['usernickname']))
    if formdata['seldepart'] != '' and formdata['seldepart'] != None:
        user_condition.children.append(('tb_user_info_department_code', formdata['seldepart']))
    if formdata['selstore'] != '' and formdata['selstore'] != None:
        user_condition.children.append(('tb_user_info_store_code', formdata['selstore']))
    rawuseridobjlist = TbUserInfo.objects.filter(user_condition).values('idtb_user_info')

    role_condition = Q()
    if formdata['selrole'] != '' and formdata['selrole'] != None:
        role_condition.children.append(('idtb_role', formdata['selrole']))
    if formdata['selrolemodule'] != '' and formdata['selrolemodule'] != None:
        role_condition.children.append(('tb_role_module_list__contains', formdata['selrolemodule']))
    if formdata['selrolefunction'] != '' and formdata['selrolefunction'] != None:
        role_condition.children.append(('tb_role_function_list__contains', formdata['selrolefunction']))
    rawroleidlist = TbRole.objects.filter(role_condition).values('idtb_role')
    uruseridobjlist = TbUserRole.objects.filter(tb_user_role_roleid__in=rawroleidlist).values('tb_user_role_userid')
    uruseridlist = []
    for uruseridobj in uruseridobjlist:
        uruseridlist.append(uruseridobj['tb_user_role_userid'])


    permission_condition = Q()
    if formdata['selpermissiontype'] != '' and formdata['selpermissiontype'] != None:
        permission_condition.children.append(('tb_permission_type_code', formdata['selpermissiontype']))
    rawpermissiontypecodelist = TbPermissionType.objects.filter(permission_condition).values('tb_permission_type_code')
    urpuseridobjlist = TbUserRolePermissionManage.objects.filter(tb_user_role_permission_manage_permission_type_code__in=rawpermissiontypecodelist).values('tb_user_role_permission_manage_user_id').distinct()
    #print(rawpermissiontypecodelist)
    urpuseridlist = []
    for urpuseridobj in urpuseridobjlist:
        urpuseridlist.append(urpuseridobj['tb_user_role_permission_manage_user_id'])
    resultcodition = Q()

    if (formdata['selrole'] != '' and formdata['selrole'] != None) or (formdata['selrolemodule'] != '' and formdata['selrolemodule'] != None) or (formdata['selrolefunction'] != '' and formdata['selrolefunction'] != None):
        resultcodition.children.append(('idtb_user_info__in', uruseridlist))
    if formdata['selpermissiontype'] != '' and formdata['selpermissiontype'] != None:
        resultcodition.children.append(('idtb_user_info__in',urpuseridlist))


    useridintersectionobjlist = rawuseridobjlist.filter(resultcodition)
    useridintersectionlist = []
    for useridintersectionobj in useridintersectionobjlist:
        useridintersectionlist.append(useridintersectionobj['idtb_user_info'])
    #print(urpuseridlist)
    #print(uruseridlist)
    #print(rawuseridobjlist)
    #print(useridintersectionlist)
    return TbUserInfo.objects.filter(idtb_user_info__in=useridintersectionlist)











