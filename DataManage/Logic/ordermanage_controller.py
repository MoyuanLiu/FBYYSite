from DataManage.models import *
from django.db.models import Q,F
from Utils.DateTimeUtil import *
import json
import time
import string

def get_order_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_order_depart_code__in',departcodelist))
    if storecodelist:
        condition.children.append(('tb_order_store_code__in', storecodelist))
    if condition.children:
        return TbOrder.objects.filter(condition)
    else:
        return TbOrder.objects.all()

def order_query(formdata):
    condition = Q()
    if formdata['queryorderdatewhetherflag']:
        condition.children.append(('tb_order_order_time__contains', formdata['queryorderdate'].strftime('%Y/%m/%d')))
    if formdata['querypaydatewhetherflag']:
        condition.children.append(('tb_order_pay_time__contains', formdata['querypaydate'].strftime('%Y/%m/%d')))
    if formdata['queryprintdatewhetherflag']:
        condition.children.append(('tb_order_print_time__contains', formdata['queryprintdate'].strftime('%Y/%m/%d')))
    if formdata['querysenddatewhetherflag']:
        condition.children.append(('tb_order_send_time__contains', formdata['querysenddate'].strftime('%Y/%m/%d')))
    if formdata['queryoverdatewhetherflag']:
        condition.children.append(('tb_order_over_time__contains', formdata['queryoverdate'].strftime('%Y/%m/%d')))
    if formdata['queryimportdatewhetherflag']:
        condition.children.append(('tb_order_pay_time__contains', formdata['queryimportdate'].strftime('%Y/%m/%d')))

    if formdata['orderclickfirmflag']:
        condition.children.append(('tb_order_click_farm_flag', formdata['orderclickfirm']))

    if formdata['orderid'] != '':
        condition.children.append(('tb_order_id', formdata['orderid']))
    if formdata['ordersysid'] != '':
        condition.children.append(('tb_order_sys_id', formdata['ordersysid']))
    if formdata['onlineproductcode'] != '':
        condition.children.append(('tb_order_online_order_status', formdata['onlineproductcode']))
    if formdata['orderdetailstatus'] != '':
        condition.children.append(('tb_order_detail_status', formdata['orderdetailstatus']))
    if formdata['queryorderdepart'] != '':
        condition.children.append(('tb_order_depart_code', formdata['queryorderdepart']))
    if formdata['queryorderstore'] != '':
        condition.children.append(('tb_order_store_code', formdata['queryorderstore']))
    query_orderlist = TbOrder.objects.filter(condition)
    return query_orderlist

def createorderimporttask(useraccount,taskcontentdict):
    createtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    expiredate = get_day_of_today(7).strftime('%Y/%m/%d')
    userid = TbUserInfo.objects.get_user_by_account(useraccount).idtb_user_info
    taskcontentstr = json.dumps(taskcontentdict, ensure_ascii=False).encode('utf-8').decode('utf-8')
    TbTaskInfo.objects.newtask('万里牛订单数据上传导入任务', '上传', taskcontentstr, userid, createtime, '任务未完成', expiredate,'orderuploadimporttask')

def createorderclickfirmimporttask(useraccount,taskcontentdict):
    createtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    expiredate = get_day_of_today(7).strftime('%Y/%m/%d')
    userid = TbUserInfo.objects.get_user_by_account(useraccount).idtb_user_info
    taskcontentstr = json.dumps(taskcontentdict, ensure_ascii=False).encode('utf-8').decode('utf-8')
    TbTaskInfo.objects.newtask('万里牛刷单数据上传导入任务', '上传', taskcontentstr, userid, createtime, '任务未完成', expiredate,'clickfirmuploadimporttask')