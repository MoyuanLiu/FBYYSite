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