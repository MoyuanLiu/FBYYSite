from DataManage.models import *
from django.db.models import Q,F
from Utils.DateTimeUtil import *
import json
import time
import string

def get_ztc_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_ztc_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_ztc_store_code__in', storecodelist))
    if condition.children:
        return TbZtc.objects.filter(condition)
    else:
        return TbZtc.objects.all()

def ztc_query(formdata):
    condition = Q()
    if formdata['ztccaldateflag']:
        condition.children.append(('tb_ztc_caldate__contains', formdata['ztccaldate'].strftime('%Y-%m-%d')))
    if formdata['ztcimportdateflag']:
        condition.children.append(('tb_ztc_import_time__contains', formdata['ztcimportdate'].strftime('%Y/%m/%d')))
    if formdata['ztcsearchtypeflag']:
        condition.children.append(('tb_ztc_search_type__in', formdata['ztcsearchtype']))
    if formdata['ztctrafficsouceflag']:
        condition.children.append(('tb_ztc_traffic_source__in', formdata['ztctrafficsouce']))
    if formdata['ztcplanname'] != '':
        condition.children.append(('tb_ztc_plan_name', formdata['ztcplanname']))
    if formdata['ztcproductname'] != '':
        condition.children.append(('tb_ztc_product_name', formdata['ztcproductname']))
    if formdata['queryztcdepart'] != '':
        condition.children.append(('tb_product_depart_id', formdata['queryztcdepart']))
    if formdata['queryztcstore'] != '':
        condition.children.append(('tb_product_store_id', formdata['queryztcstore']))
    query_ztclist = TbZtc.objects.filter(condition)
    return query_ztclist

def createztcimporttask(useraccount,taskcontentdict):
    createtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    expiredate = get_day_of_today(7).strftime('%Y/%m/%d')
    userid = TbUserInfo.objects.get_user_by_account(useraccount).idtb_user_info
    taskcontentstr = json.dumps(taskcontentdict, ensure_ascii=False).encode('utf-8').decode('utf-8')
    TbTaskInfo.objects.newtask('直通车数据上传导入任务', '上传', taskcontentstr, userid, createtime, '任务未完成', expiredate,'ztcuploadimporttask')