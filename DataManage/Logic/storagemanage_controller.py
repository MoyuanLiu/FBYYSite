from DataManage.models import *
from django.db.models import Q,F
from Utils.DateTimeUtil import *
import json
import time
import string

def get_storage_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_storage_depart_code__in',departcodelist))
    if condition.children:
        return TbStorage.objects.filter(condition)
    else:
        return TbStorage.objects.all()

def storage_query(formdata):
    condition = Q()
    if formdata['queryimportdatewhetherflag']:
        condition.children.append(('tb_storage_import_date__contains', formdata['queryimportdate'].strftime('%Y-%m-%d')))
    if formdata['storageproductid'] != '':
        condition.children.append(('tb_storage_product_id', formdata['storageproductid']))
    if formdata['storagespecname'] != '':
        condition.children.append(('tb_storage_spec_name', formdata['storagespecname']))
    if formdata['storageproductnum'] != '':
        condition.children.append(('tb_storage_product_num', formdata['storageproductnum']))
    if formdata['storagecatalogue'] != '':
        condition.children.append(('tb_storage_catalogue', formdata['storagecatalogue']))
    if formdata['querystoragedepart'] != '':
        condition.children.append(('tb_storage_depart_code', formdata['querystoragedepart']))
    query_storagelist = TbStorage.objects.filter(condition)
    return query_storagelist

def createstorageimporttask(useraccount,taskcontentdict):
    createtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    expiredate = get_day_of_today(7).strftime('%Y/%m/%d')
    userid = TbUserInfo.objects.get_user_by_account(useraccount).idtb_user_info
    taskcontentstr = json.dumps(taskcontentdict, ensure_ascii=False).encode('utf-8').decode('utf-8')
    TbTaskInfo.objects.newtask('万里牛库存数据上传导入任务', '上传', taskcontentstr, userid, createtime, '任务未完成', expiredate,'storageuploadimporttask')