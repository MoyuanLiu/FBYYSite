# -*- coding: UTF-8 -*-
from DataManage.models import *
from django.db.models import Q,F
from Utils.DateTimeUtil import *
import json
from django.core import serializers
import time

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
    if formdata['seldepart']!='':
        condition.children.append(('tb_product_depart_id', formdata['seldepart']))
    if formdata['selstore']!='':
        condition.children.append(('tb_product_store_id',  formdata['selstore']))
    query_productlist = TbProduct.objects.filter(condition)
    return query_productlist

def createproductimporttask(useraccount,taskcontentdict):
    createtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    expiredate = get_day_of_today(7).strftime('%Y/%m/%d')
    userid = TbUserInfo.objects.get_user_by_account(useraccount).idtb_user_info
    taskcontentstr = json.dumps(taskcontentdict,ensure_ascii=False).encode('utf-8').decode('utf-8')
    TbTaskInfo.objects.newtask('商品数据上传导入任务','上传',taskcontentstr,userid,createtime,'任务未完成',expiredate)

def producttask_upload_query_by_user(useraccount,taskname,tasktype,formdata):
    user = TbUserInfo.objects.get_userid_by_account(useraccount)
    userid = user.idtb_user_info

    condition = Q()
    condition.children.append(('tb_task_info_user_id', userid))
    condition.children.append(('tb_task_info_name', taskname))
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
    return TbTaskInfo.objects.filter(condition)

def producttask_upload_query_only_by_user(useraccount,taskname,tasktype):
    user = TbUserInfo.objects.get_userid_by_account(useraccount)
    userid = user.idtb_user_info
    condition = Q()
    condition.children.append(('tb_task_info_user_id', userid))
    condition.children.append(('tb_task_info_name', taskname))
    condition.children.append(('tb_task_info_type', tasktype))
    return TbTaskInfo.objects.filter(condition)

def cancel_product_uploadtask_by_taskid(taskid):
    targettask = TbTaskInfo.objects.get(idtb_task_info=taskid)
    targettask.tb_task_info_status = "任务已取消"
    canceltime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    targettask.tb_task_info_canceltime = canceltime
    targettask.save()

def cancel_product_uploadtask_check(taskid):
    targettask = TbTaskInfo.objects.get(idtb_task_info=taskid)
    if not targettask.tb_task_info_status=="任务未完成":
        return False
    else:
        return True

def getuploadfilenametasklist(tasklist):
    for task in tasklist:
        task.tb_task_info_content = json.loads(task.tb_task_info_content)["fileuploadname"]
    return tasklist

def taskuploadfilenamefilter(tasklist,filtervalue):
    if filtervalue!='':
        condition = Q()
        condition.children.append(('tb_task_info_content__contains', filtervalue))
        return tasklist.filter(condition)

