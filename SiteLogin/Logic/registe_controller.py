from django.core.cache import cache
from SiteLogin.models import *
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
