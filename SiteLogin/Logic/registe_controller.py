from django.core.cache import cache
from SiteLogin.models import *
from PermissionManage.models import TbRole
import time

def registe_departments():
    departments = TbDepartmentInfo.objects.get_all_departments()
    return departments

def registe_store_by_department(departcode):
    stores = TbStoreInfo.objects.get_all_stores_by_dapart(departcode)
    return stores

def registe_active_account(formdata):
    currentdatetime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    TbUserInfo.objects.create_new_user(formdata['username'],formdata['usernickname'],formdata['email'],formdata['pwd'],formdata['seldepart'],formdata['selstore'],1,0,currentdatetime)
    userid = TbUserInfo.objects.get_user_by_account(formdata['email']).idtb_user_info
    defaultroleid = TbRole.objects.get(tb_role_default_flag = 1).idtb_role
    TbUserRole.objects.create(tb_user_role_userid=userid,tb_user_role_roleid=defaultroleid)
