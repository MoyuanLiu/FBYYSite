from UserManage.models import *
from django.db.models import Q
import time

def get_all_departments():
    departments = TbDepartmentInfo.objects.get_all_departments()
    return departments

def update_user_edit(formdata):
    update_user = TbUserInfo.objects.get_user_by_id(formdata['userid'])
    update_user.tb_user_info_name = formdata['username']
    update_user.tb_user_info_nickname = formdata['usernickname']
    update_user.tb_user_info_email = formdata['email']
    update_user.tb_user_info_pwd = formdata['pwd']
    update_user.tb_user_info_department_code = formdata['seldepart']
    update_user.tb_user_info_store_code = formdata['selstore']
    update_user.tb_user_info_isactive = int(formdata['activeaccountwhether'])
    update_user.tb_user_info_issuperuser = int(formdata['superuserwhether'])
    update_user.save()

def user_del(userid):
    deluser = TbUserInfo.objects.get_user_by_id(userid)
    deluser.delete()

def user_add(formdata):
    currentdatetime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    TbUserInfo.objects.create_new_user(formdata['username'], formdata['usernickname'], formdata['email'],formdata['pwd'], formdata['seldepart'], formdata['selstore'], 1, formdata['superuserwhether'],currentdatetime)

def user_query(formdata):
    condition = Q()
    if formdata['querycreatedateflag']:
        condition.children.append(('tb_user_info_datejoined__contains', formdata['querycreatedate'].strftime('%Y/%m/%d')))
    if formdata['queryusername']!='' and formdata['queryusername'] != None:
        condition.children.append(('tb_user_info_name', formdata['queryusername']))
    if formdata['queryusernickname']!='' and formdata['queryusernickname'] != None:
        condition.children.append(('tb_user_info_nickname', formdata['queryusernickname']))
    if formdata['queryemail']!=''and formdata['queryemail'] != None:
        condition.children.append(('tb_user_info_email', formdata['queryemail']))
    if formdata['queryuserdepart']!='' and formdata['queryuserdepart'] != None:
        condition.children.append(('tb_user_info_department_code', formdata['queryuserdepart']))
    if formdata['queryuserstore']!='' and formdata['queryuserstore'] != None:
        condition.children.append(('tb_user_info_store_code',formdata['queryuserstore']))
    if formdata['queryactiveaccountwhetherflag']:
        condition.children.append(('tb_user_info_isactive', int(formdata['queryactiveaccountwhether'])))
    if formdata['querysuperuserwhetherflag']:
        condition.children.append(('tb_user_info_issuperuser', int(formdata['querysuperuserwhether'])))
    query_userlist = TbUserInfo.objects.filter(condition)
    return query_userlist

def update_account_edit(formdata):
    update_account = TbUserInfo.objects.get_user_by_id(formdata['userid'])
    update_account.tb_user_info_name = formdata['username']
    update_account.tb_user_info_nickname = formdata['usernickname']
    update_account.tb_user_info_department_code = formdata['seldepart']
    update_account.tb_user_info_store_code = formdata['selstore']
    update_account.save()

def renew_user_pwd(formdata):
    renew_user = TbUserInfo.objects.get_user_by_account(formdata['email'])
    renew_user.tb_user_info_pwd = formdata['pwd']
    renew_user.save()

def user_list(userlist):
    return TbUserInfo.objects.get_userinfo_list(userlist)

def eamil_change_check(formdata):
    changeuser = TbUserInfo.objects.get_user_by_id(formdata['userid'])
    if changeuser.tb_user_info_pwd == formdata['pwd']:
        return True
    else:
        return False



