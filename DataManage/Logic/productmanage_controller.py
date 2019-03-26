# -*- coding: UTF-8 -*-
from DataManage.models import *
from django.db.models import Q,F
from Utils.DateTimeUtil import *
import json
from django.core import serializers
import time
import string

def product_query(formdata):
    condition = Q()
    if formdata['productcaldatewhetherflag']:
        condition.children.append(('tb_caldate__contains',formdata['productcaldate'].strftime('%Y-%m-%d')))
    if formdata['productimportdatewhetherflag']:
        condition.children.append(('tb_product_import_time__contains', formdata['productimportdate'].strftime('%Y/%m/%d')))
    if formdata['productid']!='':
        condition.children.append(('tb_product_id', formdata['productid']))
    if formdata['productname']!='':
        condition.children.append(('tb_product_name', formdata['productname']))
    if formdata['productnum']!='':
        condition.children.append(('tb_product_num', formdata['productnum']))
    if formdata['queryproductdepart']!='':
        condition.children.append(('tb_product_depart_id', formdata['queryproductdepart']))
    if formdata['queryproductstore']!='':
        condition.children.append(('tb_product_store_id',  formdata['queryproductstore']))
    query_productlist = TbProduct.objects.filter(condition)
    return query_productlist

def createproductimporttask(useraccount,taskcontentdict):
    createtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    expiredate = get_day_of_today(7).strftime('%Y/%m/%d')
    userid = TbUserInfo.objects.get_user_by_account(useraccount).idtb_user_info
    taskcontentstr = json.dumps(taskcontentdict,ensure_ascii=False).encode('utf-8').decode('utf-8')
    TbTaskInfo.objects.newtask('商品数据上传导入任务','上传',taskcontentstr,userid,createtime,'任务未完成',expiredate,'productuploadimporttask')


def task_query(useraccount,tasknamelist,tasktype,formdata):
    user = TbUserInfo.objects.get_userid_by_account(useraccount)
    userid = user.idtb_user_info

    condition = Q()
    condition.children.append(('tb_task_info_user_id', userid))
    condition.children.append(('tb_task_info_name__in', tasknamelist))
    condition.children.append(('tb_task_info_type', tasktype))

    if formdata['taskid']!='':
        condition.children.append(('idtb_task_info', formdata['taskid']))
    if formdata['seltaskstatus']!='':
        condition.children.append(('tb_task_info_status', formdata['seltaskstatus']))
    if formdata['taskcreatedatewhetherflag']:
        condition.children.append(('tb_task_info_createtime__contains', formdata['taskcreatedate'].strftime('%Y/%m/%d')))
    if formdata['taskexpiredateewhetherflag']:
        condition.children.append(('tb_task_info_expire_date', formdata['taskexpiredate'].strftime('%Y/%m/%d')))
    if formdata['taskcanceldatewhetherflag']:
        condition.children.append(('tb_task_info_canceltime__contains', formdata['taskcanceldate'].strftime('%Y/%m/%d')))
    if formdata['taskstartdateewhetherflag']:
        condition.children.append(('tb_task_info_starttime__contains', formdata['taskstartdate'].strftime('%Y/%m/%d')))
    if formdata['taskenddateewhetherflag']:
        condition.children.append(('tb_task_info_endtime__contains', formdata['taskenddate'].strftime('%Y/%m/%d')))
    if formdata['taskuploadfilename'] and formdata['taskuploadfilename']!='':
        condition.children.append(('tb_task_info_content__contains', formdata['taskuploadfilename']))
    return TbTaskInfo.objects.filter(condition)

def task_query_only_by_user(useraccount,tasknamelist,tasktype):
    user = TbUserInfo.objects.get_userid_by_account(useraccount)
    userid = user.idtb_user_info
    condition = Q()
    condition.children.append(('tb_task_info_user_id', userid))
    condition.children.append(('tb_task_info_name__in', tasknamelist))
    condition.children.append(('tb_task_info_type', tasktype))
    return TbTaskInfo.objects.filter(condition)

def cancel_task_by_taskid(taskid):
    targettask = TbTaskInfo.objects.get(idtb_task_info=taskid)
    targettask.tb_task_info_status = "任务已取消"
    canceltime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    targettask.tb_task_info_canceltime = canceltime
    targettask.save()

def cancel_task_check(taskid):
    targettask = TbTaskInfo.objects.get(idtb_task_info=taskid)
    if not targettask.tb_task_info_status=="任务未完成":
        return False
    else:
        return True

def getuploadfilenametasklist(tasklist):
    for task in tasklist:
        taskcontentdict = {}
        taskcontentdict['fileuploadname']=(json.loads(task.tb_task_info_content)["fileuploadname"])
        taskcontentdict['savepathname'] = (json.loads(task.tb_task_info_content)["savepathname"])
        task.tb_task_info_content = taskcontentdict
    return tasklist

def get_permission_by_account(account,functioncode,permissioncode):
    user = TbUserInfo.objects.get_user_by_account(account)
    userid = user.idtb_user_info
    if userid!='':
        condition = Q()
        condition.children.append(('tb_user_role_permission_manage_user_id', userid))
        condition.children.append(('tb_user_role_permission_manage_function_code', functioncode))
        condition.children.append(('tb_user_role_permission_manage_permission_type_code', permissioncode))
        try:
            TbUserRolePermissionManageobj = TbUserRolePermissionManage.objects.get(condition)
            rangestr = TbUserRolePermissionManageobj.tb_user_role_permission_manage_permission_range
        except:
            if user.tb_user_info_issuperuser:
                rangestr = get_default_permission_rangestr()
            else:
                rangestr = ""
        permissionrangedict = parse_permission_range_str(rangestr)
        return permissionrangedict


def parse_permission_range_str(inputstr):
    range_dict = {}
    departlist = []
    storelist = []
    if inputstr=='':
        range_dict['departlist'] = departlist
        range_dict['storelist'] = storelist
    else:
        inputlist = []
        if inputstr.find(';'):
            inputlist = inputstr.split(';')
        else:
            inputlist.append(inputstr)
        for inputmsg in inputlist:
            departinputmsg = inputmsg.split('-')[0]
            departobj = TbDepartmentInfo.objects.get(tb_department_info_code=departinputmsg)
            storeinputmsg = inputmsg.split('-')[1]
            if not departobj in departlist:
                departlist.append(departobj)
            if storeinputmsg == 'All':
                allstoreobjs = TbStoreInfo.objects.filter(tb_store_info_department_code=departinputmsg)
                for allstoreobj in allstoreobjs:
                    if not allstoreobj in storelist:
                        storelist.append(allstoreobj)
            else:
                storeobj = TbStoreInfo.objects.get(tb_store_code=storeinputmsg)
                if not storeobj in storelist:
                    storelist.append(storeobj)
        range_dict['departlist'] = departlist
        range_dict['storelist'] = storelist
    return range_dict

def get_product_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_product_depart_id__in',departcodelist))
    if storecodelist:
        condition.children.append(('tb_product_store_id__in', storecodelist))
    if condition.children:
        return TbProduct.objects.filter(condition)
    else:
        return TbProduct.objects.all()

def get_default_permission_rangestr():
    default_rangestr = ""
    for departinfo in TbDepartmentInfo.objects.all():
        default_rangestr+=departinfo.tb_department_info_code + "-All;"
    default_rangestr = default_rangestr.strip(string.punctuation)
    return default_rangestr

def get_departments_by_permission(permissiondepartlist):
    if permissiondepartlist:
        return TbDepartmentInfo.objects.filter(tb_department_info_code__in=permissiondepartlist)
    else:
        return TbDepartmentInfo.objects.all()

def get_store_by_department(departcode,storelist):
    resultstorelist = []
    condition = Q()
    if departcode!='':
        condition.children.append(('tb_store_info_department_code', departcode))
    for storeobj in TbStoreInfo.objects.filter(condition):
        for perstoreobj in storelist:
            if storeobj == perstoreobj:
                resultstorelist.append(storeobj)
    return resultstorelist

def get_permission_store_code_list(storeobjlist):
    storecodelist = []
    if storeobjlist:
        for storeobj in storeobjlist:
            storecodelist.append(storeobj.tb_store_code)
    else:
        for storeinfoobj in TbStoreInfo.objects.all():
            storecodelist.append(storeinfoobj.tb_store_code)
    return storecodelist

def get_permission_depart_code_list(departobjlist):
    departcodelist = []
    if departobjlist:
        for departobj in departobjlist:
            departcodelist.append(departobj.tb_department_info_code)
    else:
        for departinfoobj in TbDepartmentInfo.objects.all():
            departcodelist.append(departinfoobj.tb_department_info_code)
    return departcodelist
















