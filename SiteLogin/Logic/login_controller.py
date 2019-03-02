from django.core.cache import cache
from SiteLogin.models import *

def isauthenticated(account):
    if cache.get(account) == None:
        return False
    else:
        return True

def logincheck(account,password,rem):
    flag = False
    if account != '':
        user = TbUserInfo.objects.get_user_by_account(account)
        if user != None:
            if user.tb_user_info_pwd == password:
                if rem:
                    cache.set(account, password, 14 * 24 * 60 * 60)
                else:
                    cache.set(account,password,24*60*60)
                flag = True
    return flag

def login_update(account,currenttime):
    user = TbUserInfo.objects.get_user_by_account(account)
    if user != None:
        user.tb_user_info_last_login = currenttime
        user.save()

def user_permission_check(account):
    user = TbUserInfo.objects.get_user_by_account(account)
    if user.tb_user_info_issuperuser == 1:
        return True
    else:
        return False

def get_user_role_name(account):
    user = TbUserInfo.objects.get_user_by_account(account)
    roleid = TbUserRole.objects.get_user_role_by_user_id(user.idtb_user_info).tb_user_role_roleid
    return TbRole.objects.get_role_name_by_role_id(roleid)

def get_all_modules():
    return TbModule.objects.get_all_modules_list()

def get_all_functions():
    return TbFunction.objects.get_all_functions_list()

def get_user_modules(account):
    user = TbUserInfo.objects.get_user_by_account(account)
    if user != None:
        userid = user.idtb_user_info
        roleid = TbUserRole.objects.get_user_role_by_user_id(userid).tb_user_role_roleid
        roleobj = TbRole.objects.get(idtb_role=roleid)
        return TbModule.objects.filter(tb_module_code__in=eval(roleobj.tb_role_module_list))


def get_user_functions(account):
    user = TbUserInfo.objects.get_user_by_account(account)
    if user != None:
        userid = user.idtb_user_info
        roleid = TbUserRole.objects.get_user_role_by_user_id(userid).tb_user_role_roleid
        roleobj = TbRole.objects.get(idtb_role=roleid)
        return TbFunction.objects.filter(tb_function_code__in=eval(roleobj.tb_role_function_list))
