import time
import json
from DataManage.models import *
from django.db.models import Q, F
import os
import configparser
import xlrd
import operator
from Utils.FileOptUtil import *
from Utils.StringUtil import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction



def expiretaskbyexpiredate():
    print("检查过期任务")
    curdate = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    expiretaskcondition = Q()
    expiretaskcondition.children.append(('tb_task_info_expire_date__lt', curdate))
    expiretasklist = TbTaskInfo.objects.filter(expiretaskcondition)
    for expiretask in expiretasklist:
        expiretask.tb_task_info_status = '任务已过期'
        tasksavefilepath = json.loads(expiretask.tb_task_info_content)["savepath"]
        if os.path.isfile(tasksavefilepath):
            os.remove(tasksavefilepath)
            print("过期任务文件已移除")
            expiretask.save()


def runimporttask(taskobj):
    cf = configparser.ConfigParser()
    cf.read("Conf/project.conf", encoding='UTF-8')
    checklistdirlist = []
    taskcode = taskobj.tb_task_info_code
    if taskobj.tb_task_info_code != 'productuploadimporttask':
        taskchecklistconfstr = 'CSD_' + taskcode
        checklistdir = cf.get('ImportCheckServicesDir', taskchecklistconfstr)
        checklistdirlist.append(checklistdir)
    else:
        taskchecklistconfstr1 = 'CSD_' + taskcode
        taskchecklistconfstr2 = 'CSD_old' + taskcode
        checklistdir = cf.get('ImportCheckServicesDir', taskchecklistconfstr1)
        oldchecklistdir = cf.get('ImportCheckServicesDir', taskchecklistconfstr2)
        checklistdirlist.append(checklistdir)
        checklistdirlist.append(oldchecklistdir)
    taskpath = json.loads(taskobj.tb_task_info_content)["savepath"]

    tableheadrownum = int(cf.get('ImportCheckStartRow', 'CSR_' + taskcode))
    if os.path.isfile(taskpath):
        data = xlrd.open_workbook(taskpath)
        table = data.sheets()[0]
        if columncheck(table.row(tableheadrownum), checklistdirlist):
            print('通过校验')
            importmethoddistribute(taskobj, table, tableheadrownum)
        else:
            curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            taskobj.tb_task_info_status = '任务已失败'
            taskobj.tb_task_info_endtime = curtime
            taskobj.save()





def columncheck(tablehead, checklistdirlist):
    flag = False
    tableheadlist = []
    for th in tablehead:
        tableheadlist.append(th.value)
    for checklistdir in checklistdirlist:
        print(readfileaslist(checklistdir))
        print(tableheadlist)
        if operator.eq(readfileaslist(checklistdir), tableheadlist):
            flag = True
    return flag


def importmethoddistribute(taskobj, tabledata, tableheadrownum, ):
    print('分配处理任务')
    taskcode = taskobj.tb_task_info_code
    if taskcode == 'productuploadimporttask':
        if isOldProductOrNot(tabledata, tableheadrownum):
            importoldproductdata(tabledata, tableheadrownum, taskobj)
        else:
            importproductdata(tabledata, tableheadrownum, taskobj)
    if taskcode == 'ztcuploadimporttask':
        importztcdata(tabledata, tableheadrownum, taskobj)
    if taskcode == 'orderuploadimporttask':
        importorderdata(tabledata, tableheadrownum, taskobj)
    if taskcode == 'clickfirmuploadimporttask':
        importclickfirmdata(tabledata, tableheadrownum, taskobj)
    if taskcode == 'storageuploadimporttask':
        importstoragedata(tabledata, tableheadrownum, taskobj)
    if taskcode == 'storeuploadimporttask':
        importstoredata(tabledata, tableheadrownum, taskobj)


def isOldProductOrNot(tabledata, tableheadrownum):
    flag = False
    cf = configparser.ConfigParser()
    cf.read("../Conf/project.conf", encoding='UTF-8')
    oldproductchecklistdir = cf.get('ImportCheckServicesDir', 'CSD_oldproductuploadimporttask')
    oldproductchecklist = readfileaslist(oldproductchecklistdir)
    if operator.eq(oldproductchecklist, tabledata.row(tableheadrownum)):
        flag = True
    return flag


def importproductdata(tabledata, tableheadrownum, taskobj):
    flag = True
    nrows = tabledata.nrows
    taskfilename = json.loads(taskobj.tb_task_info_content)["savepathname"]
    departcode = taskfilename.split('-')[0].upper()
    storecode = taskfilename.split('-')[1].upper()
    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status='任务进行中'
    taskobj.tb_task_info_starttime=curtime
    taskobj.save()

    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        querycondition = Q()
        querycondition.children.append(('tb_caldate', tabledata.row(i)[0].value))
        querycondition.children.append(('tb_product_store_id', storecode))
        querycondition.children.append(('tb_product_id', tabledata.row(i)[1].value))
        try:
            updateproduct = TbProduct.objects.get(querycondition)
            updatedata = {}
            updatedata['tb_product_name'] = tabledata.row(i)[2].value
            updatedata['tb_product_num'] = tabledata.row(i)[3].value
            updatedata['tb_product_product_status'] = tabledata.row(i)[4].value
            updatedata['tb_product_product_tag'] = tabledata.row(i)[5].value
            updatedata['tb_product_visitors'] = changeStrtoInt(tabledata.row(i)[6].value)
            updatedata['tb_product_views'] = changeStrtoInt(tabledata.row(i)[7].value)
            updatedata['tb_avg_stoptime'] = changeStrtoFloat(tabledata.row(i)[8].value)
            updatedata['tb_detail_page_jump_percent'] = changeStrtoPercent(tabledata.row(i)[9].value)
            updatedata['tb_product_collects'] = changeStrtoInt(tabledata.row(i)[10].value)
            updatedata['tb_product_join_items'] = changeStrtoInt(tabledata.row(i)[11].value)
            updatedata['tb_product_joins'] = changeStrtoInt(tabledata.row(i)[12].value)
            updatedata['tb_product_order_buyyers'] = changeStrtoInt(tabledata.row(i)[13].value)
            updatedata['tb_product_buy_order_items'] = changeStrtoInt(tabledata.row(i)[14].value)
            updatedata['tb_product_buy_order_money'] = changeStrtoFloat(tabledata.row(i)[15].value)
            updatedata['tb_product_order_converse_percent'] = changeStrtoPercent(tabledata.row(i)[16].value)
            updatedata['tb_product_payers'] = changeStrtoInt(tabledata.row(i)[17].value)
            updatedata['tb_product_pay_items'] = changeStrtoInt(tabledata.row(i)[18].value)
            updatedata['tb_product_pay_money'] = changeStrtoFloat(tabledata.row(i)[19].value)
            updatedata['tb_product_pay_converse_percent'] =changeStrtoPercent(tabledata.row(i)[20].value)
            updatedata['tb_product_new_payyers'] = changeStrtoInt(tabledata.row(i)[21].value)
            updatedata['tb_product_old_payyers'] = changeStrtoInt(tabledata.row(i)[22].value)
            updatedata['tb_product_old_payyer_money'] = changeStrtoFloat(tabledata.row(i)[23].value)
            updatedata['tb_product_juhuasuan_money'] = changeStrtoFloat(tabledata.row(i)[24].value)
            updatedata['tb_product_avg_value_visitors'] = changeStrtoFloat(tabledata.row(i)[25].value)
            updatedata['tb_product_sell_return_money'] = changeStrtoFloat(tabledata.row(i)[26].value)
            updatedata['tb_product_compare_score'] = changeStrtoFloat(tabledata.row(i)[27].value)
            updatedata['tb_product_count_year_money'] = changeStrtoFloat(tabledata.row(i)[28].value)
            updatedata['tb_product_count_month_money'] = changeStrtoFloat(tabledata.row(i)[29].value)
            updatedata['tb_product_count_month_items'] = changeStrtoInt(tabledata.row(i)[30].value)
            updatedata['tb_product_search_into_pay_percent'] = changeStrtoPercent(tabledata.row(i)[31].value)
            updatedata['tb_product_search_into_visitors'] = changeStrtoInt(tabledata.row(i)[32].value)
            updatedata['tb_product_search_into_pay_buyyers'] = changeStrtoInt(tabledata.row(i)[33].value)
            updateproduct.__dict__.update(updatedata)
            updateproduct.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbProduct.objects.create(tb_caldate=tabledata.row(i)[0].value, tb_product_id=tabledata.row(i)[1].value,
                                     tb_product_name=tabledata.row(i)[2].value,
                                     tb_product_num=tabledata.row(i)[3].value,
                                     tb_product_product_status=tabledata.row(i)[4].value,
                                     tb_product_product_tag=tabledata.row(i)[5].value,
                                     tb_product_visitors=changeStrtoInt(tabledata.row(i)[6].value),
                                     tb_product_views=changeStrtoInt(tabledata.row(i)[7].value),
                                     tb_avg_stoptime=changeStrtoFloat(tabledata.row(i)[8].value),
                                     tb_detail_page_jump_percent=changeStrtoPercent(tabledata.row(i)[9].value),
                                     tb_product_collects=changeStrtoInt(tabledata.row(i)[10].value),
                                     tb_product_join_items=changeStrtoInt(tabledata.row(i)[11].value),
                                     tb_product_joins=changeStrtoInt(tabledata.row(i)[12].value),
                                     tb_product_order_buyyers=changeStrtoInt(tabledata.row(i)[13].value),
                                     tb_product_buy_order_items=changeStrtoInt(tabledata.row(i)[14].value),
                                     tb_product_buy_order_money=changeStrtoFloat(tabledata.row(i)[15].value),
                                     tb_product_order_converse_percent=changeStrtoPercent(tabledata.row(i)[16].value),
                                     tb_product_payers=changeStrtoInt(tabledata.row(i)[17].value),
                                     tb_product_pay_items=changeStrtoInt(tabledata.row(i)[18].value),
                                     tb_product_pay_money=changeStrtoFloat(tabledata.row(i)[19].value),
                                     tb_product_pay_converse_percent=changeStrtoPercent(tabledata.row(i)[20].value),
                                     tb_product_new_payyers=changeStrtoInt(tabledata.row(i)[21].value),
                                     tb_product_old_payyers=changeStrtoInt(tabledata.row(i)[22].value),
                                     tb_product_old_payyer_money=changeStrtoFloat(tabledata.row(i)[23].value),
                                     tb_product_juhuasuan_money=changeStrtoFloat(tabledata.row(i)[24].value),
                                     tb_product_avg_value_visitors=changeStrtoFloat(tabledata.row(i)[25].value),
                                     tb_product_sell_return_money=changeStrtoFloat(tabledata.row(i)[26].value),
                                     tb_product_compare_score=changeStrtoFloat(tabledata.row(i)[27].value),
                                     tb_product_count_year_money=changeStrtoFloat(tabledata.row(i)[28].value),
                                     tb_product_count_month_money=changeStrtoFloat(tabledata.row(i)[29].value),
                                     tb_product_count_month_items=changeStrtoInt(tabledata.row(i)[30].value),
                                     tb_product_store_id=storecode,
                                     tb_product_search_into_pay_percent=changeStrtoPercent(tabledata.row(i)[31].value),
                                     tb_product_search_into_visitors=changeStrtoInt(tabledata.row(i)[32].value),
                                     tb_product_search_into_pay_buyyers=changeStrtoInt(tabledata.row(i)[33].value),
                                     tb_product_depart_id=departcode,
                                     tb_product_import_time=currenttime)
        except:
            flag = False
            break

    if flag:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已完成'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()
    else:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已失败'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()


def importoldproductdata(tabledata, tableheadrownum, taskobj):
    flag = True
    nrows = tabledata.nrows
    taskfilename = json.loads(taskobj.tb_task_info_content)["savepathname"]
    departcode = taskfilename.split('-')[0].upper()
    storecode = taskfilename.split('-')[1].upper()
    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status='任务进行中'
    taskobj.tb_task_info_starttime=curtime
    taskobj.save()

    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        querycondition = Q()
        querycondition.children.append(('tb_caldate', tabledata.row(i)[0].value))
        querycondition.children.append(('tb_product_store_id', storecode))
        querycondition.children.append(('tb_product_id', tabledata.row(i)[1].value))
        try:
            updateproduct = TbProduct.objects.get(querycondition)
            updatedata = {}
            updatedata['tb_product_name'] = tabledata.row(i)[2].value
            updatedata['tb_product_num'] = tabledata.row(i)[3].value
            updatedata['tb_product_visitors'] = changeStrtoInt(tabledata.row(i)[4].value)
            updatedata['tb_product_views'] = changeStrtoInt(tabledata.row(i)[5].value)
            updatedata['tb_avg_stoptime'] = changeStrtoFloat(tabledata.row(i)[6].value)
            updatedata['tb_detail_page_jump_percent'] = changeStrtoPercent(tabledata.row(i)[7].value)
            updatedata['tb_product_collects'] = changeStrtoInt(tabledata.row(i)[8].value)
            updatedata['tb_product_join_items'] = changeStrtoInt(tabledata.row(i)[9].value)
            updatedata['tb_product_order_buyyers'] = changeStrtoInt(tabledata.row(i)[10].value)
            updatedata['tb_product_buy_order_items'] = changeStrtoInt(tabledata.row(i)[11].value)
            updatedata['tb_product_buy_order_money'] = changeStrtoFloat(tabledata.row(i)[12].value)
            updatedata['tb_product_order_converse_percent'] = changeStrtoPercent(tabledata.row(i)[13].value)
            updatedata['tb_product_payers'] = changeStrtoInt(tabledata.row(i)[14].value)
            updatedata['tb_product_pay_items'] = changeStrtoInt(tabledata.row(i)[15].value)
            updatedata['tb_product_pay_money'] = changeStrtoFloat(tabledata.row(i)[16].value)
            updatedata['tb_product_pay_converse_percent'] = changeStrtoPercent(tabledata.row(i)[17].value)
            updatedata['tb_product_avg_value_visitors'] = changeStrtoFloat(tabledata.row(i)[18].value)
            updatedata['tb_product_sell_return_money'] = changeStrtoFloat(tabledata.row(i)[19].value)
            updateproduct.__dict__.update(updatedata)
            updateproduct.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbProduct.objects.create(tb_caldate=tabledata.row(i)[0].value, tb_product_id=tabledata.row(i)[1].value,
                                     tb_product_name=tabledata.row(i)[2].value,
                                     tb_product_num=tabledata.row(i)[3].value,
                                     tb_product_visitors=changeStrtoInt(tabledata.row(i)[4].value),
                                     tb_product_views=changeStrtoInt(tabledata.row(i)[5].value),
                                     tb_avg_stoptime=changeStrtoFloat(tabledata.row(i)[6].value),
                                     tb_detail_page_jump_percent=changeStrtoPercent(tabledata.row(i)[7].value),
                                     tb_product_collects=changeStrtoInt(tabledata.row(i)[8].value),
                                     tb_product_join_items=changeStrtoInt(tabledata.row(i)[9].value),
                                     tb_product_order_buyyers=changeStrtoInt(tabledata.row(i)[10].value),
                                     tb_product_buy_order_items=changeStrtoInt(tabledata.row(i)[11].value),
                                     tb_product_buy_order_money=changeStrtoFloat(tabledata.row(i)[12].value),
                                     tb_product_order_converse_percent=changeStrtoPercent(tabledata.row(i)[13].value),
                                     tb_product_payers=changeStrtoInt(tabledata.row(i)[14].value),
                                     tb_product_pay_items=changeStrtoInt(tabledata.row(i)[15].value),
                                     tb_product_pay_money=changeStrtoFloat(tabledata.row(i)[16].value),
                                     tb_product_pay_converse_percent=changeStrtoPercent(tabledata.row(i)[17].value),
                                     tb_product_avg_value_visitors=changeStrtoFloat(tabledata.row(i)[18].value),
                                     tb_product_sell_return_money=changeStrtoFloat(tabledata.row(i)[19].value),
                                     tb_product_store_id=storecode, tb_product_depart_id=departcode,
                                     tb_product_import_time=currenttime)
        except:
            flag = False
            break

    if flag:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已完成'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()
    else:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已失败'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()


def importztcdata(tabledata, tableheadrownum, taskobj):
    flag = True
    nrows = tabledata.nrows
    taskfilename = json.loads(taskobj.tb_task_info_content)["savepathname"]
    departcode = taskfilename.split('-')[0].upper()
    storecode = taskfilename.split('-')[1].upper()
    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status='任务进行中'
    taskobj.tb_task_info_starttime=curtime
    taskobj.save()

    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        querycondition = Q()
        querycondition.children.append(('tb_ztc_caldate', changeExcelDate(tabledata.row(i)[0].value)))
        querycondition.children.append(('tb_ztc_plan_name', tabledata.row(i)[1].value))
        querycondition.children.append(('tb_ztc_product_name', tabledata.row(i)[2].value))
        querycondition.children.append(('tb_ztc_search_type', tabledata.row(i)[3].value))
        querycondition.children.append(('tb_ztc_traffic_source', tabledata.row(i)[4].value))
        querycondition.children.append(('tb_ztc_store_code', storecode))
        try:
            updateztc = TbZtc.objects.get(querycondition)
            updatedata = {}
            updatedata['tb_ztc_impression_count'] = fixStoreName(tabledata.row(i)[0].value)
            updatedata['tb_ztc_click_count'] = tabledata.row(i)[2].value
            updatedata['tb_ztc_cost'] = tabledata.row(i)[3].value
            updatedata['tb_ztc_click_percent'] = fixNullNumber(tabledata.row(i)[4].value)
            updatedata['tb_ztc_avg_click_cost'] = fixNullNumber(tabledata.row(i)[5].value)
            updatedata['tb_ztc_thousand_impression_cost'] = tabledata.row(i)[6].value
            updatedata['tb_ztc_click_turn_percent'] = tabledata.row(i)[7].value
            updatedata['tb_ztc_direct_deal_money'] = fixSymbol(tabledata.row(i)[8].value)
            updatedata['tb_ztc_direct_deal_count'] = fixchangeline(tabledata.row(i)[9].value)
            updatedata['tb_ztc_undirect_deal_money'] = tabledata.row(i)[10].value
            updatedata['tb_ztc_undirect_deal_count'] = tabledata.row(i)[11].value
            updatedata['tb_ztc_deal_money'] = tabledata.row(i)[12].value
            updatedata['tb_ztc_deal_count'] = tabledata.row(i)[13].value
            updatedata['tb_ztc_product_collect_count'] = tabledata.row(i)[14].value
            updatedata['tb_ztc_store_collect_count'] = tabledata.row(i)[15].value
            updatedata['tb_ztc_io_ratio'] = tabledata.row(i)[16].value
            updatedata['tb_ztc_direct_cart_count'] = tabledata.row(i)[17].value
            updatedata['tb_ztc_undirect_cart_count'] = removespace(tabledata.row(i)[18].value)
            updatedata['tb_ztc_total_cart_count'] = tabledata.row(i)[19].value
            updateztc.__dict__.update(updatedata)
            updateztc.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbZtc.objects.create(tb_ztc_caldate=changeExcelDate(tabledata.row(i)[0].value),
                                 tb_ztc_plan_name=tabledata.row(i)[1].value,
                                 tb_ztc_product_name=tabledata.row(i)[2].value,
                                 tb_ztc_search_type=tabledata.row(i)[3].value,
                                 tb_ztc_traffic_source=tabledata.row(i)[4].value,
                                 tb_ztc_impression_count=fixNull(tabledata.row(i)[5].value),
                                 tb_ztc_click_count=fixNull(tabledata.row(i)[6].value),
                                 tb_ztc_cost=fixNull(tabledata.row(i)[7].value),
                                 tb_ztc_click_percent=fixNull(tabledata.row(i)[8].value),
                                 tb_ztc_avg_click_cost=fixNull(tabledata.row(i)[9].value),
                                 tb_ztc_thousand_impression_cost=fixNull(tabledata.row(i)[10].value),
                                 tb_ztc_click_turn_percent=fixNull(tabledata.row(i)[11].value),
                                 tb_ztc_direct_deal_money=fixNull(tabledata.row(i)[12].value),
                                 tb_ztc_direct_deal_count=fixNull(tabledata.row(i)[13].value),
                                 tb_ztc_undirect_deal_money=fixNull(tabledata.row(i)[14].value),
                                 tb_ztc_undirect_deal_count=fixNull(tabledata.row(i)[15].value),
                                 tb_ztc_deal_money=fixNull(tabledata.row(i)[16].value),
                                 tb_ztc_deal_count=fixNull(tabledata.row(i)[17].value),
                                 tb_ztc_product_collect_count=fixNull(tabledata.row(i)[18].value),
                                 tb_ztc_store_collect_count=fixNull(tabledata.row(i)[19].value),
                                 tb_ztc_total_collect_count=fixNull(tabledata.row(i)[20].value),
                                 tb_ztc_io_ratio=fixNull(tabledata.row(i)[21].value),
                                 tb_ztc_direct_cart_count=fixNull(tabledata.row(i)[22].value),
                                 tb_ztc_undirect_cart_count=fixNull(tabledata.row(i)[23].value),
                                 tb_ztc_total_cart_count=fixNull(tabledata.row(i)[24].value),
                                 tb_ztc_store_code=storecode, tb_ztc_depart_code=departcode,
                                 tb_ztc_import_time=currenttime)
        except:
            flag = False
            break

    if flag:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已完成'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()
    else:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已失败'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()

def importorderdata(tabledata, tableheadrownum, taskobj):
    flag = True
    nrows = tabledata.nrows
    taskfilename = json.loads(taskobj.tb_task_info_content)["savepathname"]
    departcode = taskfilename.split('-')[0].upper()
    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status='任务进行中'
    taskobj.tb_task_info_starttime=curtime
    taskobj.save()

    orderobjlist = []
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        #querycondition = Q()
        orderdatestr = getdatestr(tabledata.row(i)[53].value)
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        try:
            curorder = TbOrder(tb_order_store_name=fixStoreName(tabledata.row(i)[0].value),
                               tb_order_id=tabledata.row(i)[1].value, tb_order_sys_id=tabledata.row(i)[2].value,
                               tb_order_mark=tabledata.row(i)[3].value,
                               tb_order_actual_pay_count=fixNullNumber(tabledata.row(i)[4].value),
                               tb_order_benifit_count=fixNullNumber(tabledata.row(i)[5].value),
                               tb_order_storage_code=tabledata.row(i)[6].value,
                               tb_order_storage_name=tabledata.row(i)[7].value,
                               tb_order_buyyer_review=fixSymbol(tabledata.row(i)[8].value),
                               tb_order_comment=fixchangeline(tabledata.row(i)[9].value),
                               tb_order_print_comment=tabledata.row(i)[10].value,
                               tb_order_sys_order_status=tabledata.row(i)[11].value,
                               tb_order_online_order_status=tabledata.row(i)[12].value,
                               tb_order_patch_num=tabledata.row(i)[13].value,
                               tb_order_detail_status=tabledata.row(i)[14].value,
                               tb_order_old_order_id=tabledata.row(i)[15].value,
                               tb_order_product_code=tabledata.row(i)[16].value,
                               tb_order_product_name=tabledata.row(i)[17].value,
                               tb_order_spec_name=removespace(tabledata.row(i)[18].value),
                               tb_order_online_product_code=tabledata.row(i)[19].value,
                               tb_order_online_product_title=tabledata.row(i)[20].value,
                               tb_order_online_spec=tabledata.row(i)[21].value,
                               tb_order_price=tabledata.row(i)[22].value,
                               tb_order_benifit_price=tabledata.row(i)[23].value,
                               tb_order_num=tabledata.row(i)[24].value, tb_order_unit=tabledata.row(i)[25].value,
                               tb_order_suppose_money=tabledata.row(i)[26].value,
                               tb_order_sale_money=tabledata.row(i)[27].value,
                               tb_order_detail_comment=tabledata.row(i)[28].value,
                               tb_order_invoice_title=tabledata.row(i)[29].value,
                               tb_order_invoice_content=tabledata.row(i)[30].value,
                               tb_order_invoice_bank=tabledata.row(i)[31].value,
                               tb_order_invoice_bank_account=tabledata.row(i)[32].value,
                               tb_order_invoice_tax_number=tabledata.row(i)[33].value,
                               tb_order_invoice_address=tabledata.row(i)[34].value,
                               tb_order_invoice_tel=tabledata.row(i)[35].value,
                               tb_order_invoice_email=tabledata.row(i)[36].value,
                               tb_order_express_company=tabledata.row(i)[37].value,
                               tb_order_express_num=tabledata.row(i)[38].value,
                               tb_order_express_cost=changeStrtoFloat(tabledata.row(i)[39].value),
                               tb_order_weight=changeStrtoFloat(tabledata.row(i)[40].value),
                               tb_order_volume=changeStrtoFloat(tabledata.row(i)[41].value),
                               tb_order_post_cost=fixNullNumber(tabledata.row(i)[42].value),
                               tb_order_service_cost=fixNullNumber(tabledata.row(i)[43].value),
                               tb_order_account=tabledata.row(i)[44].value,
                               tb_order_receiver_name=fixSymbol(tabledata.row(i)[45].value),
                               tb_order_idcard_num=tabledata.row(i)[46].value,
                               tb_order_receiver_tel=tabledata.row(i)[47].value,
                               tb_order_receiver_province=tabledata.row(i)[48].value,
                               tb_order_receiver_city=tabledata.row(i)[49].value,
                               tb_order_receiver_county=tabledata.row(i)[50].value,
                               tb_order_receiver_detail_address=fixSymbol(tabledata.row(i)[51].value),
                               tb_order_post_code=tabledata.row(i)[52].value,
                               tb_order_order_time=tabledata.row(i)[53].value,
                               tb_order_pay_time=tabledata.row(i)[54].value,
                               tb_order_print_time=tabledata.row(i)[55].value,
                               tb_order_send_time=tabledata.row(i)[56].value,
                               tb_order_over_time=tabledata.row(i)[57].value,
                               tb_order_trade_hire_money=fixNullNumber(tabledata.row(i)[58].value),
                               tb_order_cdcard_hire_money=fixNullNumber(tabledata.row(i)[59].value),
                               tb_order_return_score=changeStrtoFloat(tabledata.row(i)[60].value),
                               tb_order_checker=tabledata.row(i)[61].value,
                               tb_order_printer=tabledata.row(i)[62].value,
                               tb_order_distributor=tabledata.row(i)[63].value,
                               tb_order_surveyor=tabledata.row(i)[64].value,
                               tb_order_packer=tabledata.row(i)[65].value,
                               tb_order_weighter=tabledata.row(i)[66].value,
                               tb_order_sender=tabledata.row(i)[67].value,
                               tb_order_salesman=tabledata.row(i)[68].value,
                               tb_order_order_date=orderdatestr,
                               tb_order_store_code=getstorecodebyname(tabledata.row(i)[0].value), tb_order_depart_code=departcode,
                               tb_order_import_time=currenttime)
            orderobjlist.append(curorder)
        except Exception as err:
            print(err)
            flag = False
            break
    TbOrder.objects.bulk_create(orderobjlist)
    orderobjlist.clear()
    print('提交数据')
    if flag:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已完成'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()
    else:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已失败'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()

def importclickfirmdata(tabledata, tableheadrownum, taskobj):
    flag = True
    nrows = tabledata.nrows
    taskfilename = json.loads(taskobj.tb_task_info_content)["savepathname"]
    departcode = taskfilename.split('-')[0].upper()

    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status='任务进行中'
    taskobj.tb_task_info_starttime=curtime
    taskobj.save()
    orderobjlist = []
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        orderdatequery = getdatestr(tabledata.row(i)[53].value)
        orderidquery = tabledata.row(i)[1].value
        orderproductcode = tabledata.row(i)[19].value
        querycondition = Q()
        querycondition.children.append(('tb_order_order_date', orderdatequery))
        querycondition.children.append(('tb_order_id', orderidquery))
        querycondition.children.append(('tb_order_online_product_code', orderproductcode))
        try:
            updateorder = TbOrder.objects.get(querycondition)
            updatedata = {}
            updatedata['tb_order_click_farm_flag'] = 1
            updateorder.__dict__.update(updatedata)
            updateorder.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            curorder = TbOrder(tb_order_store_name=fixStoreName(tabledata.row(i)[0].value),
                                   tb_order_id=orderidquery, tb_order_sys_id=tabledata.row(i)[2].value,
                                   tb_order_mark=tabledata.row(i)[3].value,
                                   tb_order_actual_pay_count=fixNullNumber(tabledata.row(i)[4].value),
                                   tb_order_benifit_count=fixNullNumber(tabledata.row(i)[5].value),
                                   tb_order_storage_code=tabledata.row(i)[6].value,
                                   tb_order_storage_name=tabledata.row(i)[7].value,
                                   tb_order_buyyer_review=fixSymbol(tabledata.row(i)[8].value),
                                   tb_order_comment=fixchangeline(tabledata.row(i)[9].value),
                                   tb_order_print_comment=tabledata.row(i)[10].value,
                                   tb_order_sys_order_status=tabledata.row(i)[11].value,
                                   tb_order_online_order_status=tabledata.row(i)[12].value,
                                   tb_order_patch_num=tabledata.row(i)[13].value,
                                   tb_order_detail_status=tabledata.row(i)[14].value,
                                   tb_order_old_order_id=tabledata.row(i)[15].value,
                                   tb_order_product_code=tabledata.row(i)[16].value,
                                   tb_order_product_name=tabledata.row(i)[17].value,
                                   tb_order_spec_name=removespace(tabledata.row(i)[18].value),
                                   tb_order_online_product_code=orderproductcode,
                                   tb_order_online_product_title=tabledata.row(i)[20].value,
                                   tb_order_online_spec=tabledata.row(i)[21].value,
                                   tb_order_price=tabledata.row(i)[22].value,
                                   tb_order_benifit_price=tabledata.row(i)[23].value,
                                   tb_order_num=tabledata.row(i)[24].value, tb_order_unit=tabledata.row(i)[25].value,
                                   tb_order_suppose_money=tabledata.row(i)[26].value,
                                   tb_order_sale_money=tabledata.row(i)[27].value,
                                   tb_order_detail_comment=tabledata.row(i)[28].value,
                                   tb_order_invoice_title=tabledata.row(i)[29].value,
                                   tb_order_invoice_content=tabledata.row(i)[30].value,
                                   tb_order_invoice_bank=tabledata.row(i)[31].value,
                                   tb_order_invoice_bank_account=tabledata.row(i)[32].value,
                                   tb_order_invoice_tax_number=tabledata.row(i)[33].value,
                                   tb_order_invoice_address=tabledata.row(i)[34].value,
                                   tb_order_invoice_tel=tabledata.row(i)[35].value,
                                   tb_order_invoice_email=tabledata.row(i)[36].value,
                                   tb_order_express_company=tabledata.row(i)[37].value,
                                   tb_order_express_num=tabledata.row(i)[38].value,
                                   tb_order_express_cost=changeStrtoFloat(tabledata.row(i)[39].value),
                                   tb_order_weight=changeStrtoFloat(tabledata.row(i)[40].value),
                                   tb_order_volume=changeStrtoFloat(tabledata.row(i)[41].value),
                                   tb_order_post_cost=fixNullNumber(tabledata.row(i)[42].value),
                                   tb_order_service_cost=fixNullNumber(tabledata.row(i)[43].value),
                                   tb_order_account=tabledata.row(i)[44].value,
                                   tb_order_receiver_name=fixSymbol(tabledata.row(i)[45].value),
                                   tb_order_idcard_num=tabledata.row(i)[46].value,
                                   tb_order_receiver_tel=tabledata.row(i)[47].value,
                                   tb_order_receiver_province=tabledata.row(i)[48].value,
                                   tb_order_receiver_city=tabledata.row(i)[49].value,
                                   tb_order_receiver_county=tabledata.row(i)[50].value,
                                   tb_order_receiver_detail_address=fixSymbol(tabledata.row(i)[51].value),
                                   tb_order_post_code=tabledata.row(i)[52].value,
                                   tb_order_order_time=tabledata.row(i)[53].value,
                                   tb_order_pay_time=tabledata.row(i)[54].value,
                                   tb_order_print_time=tabledata.row(i)[55].value,
                                   tb_order_send_time=tabledata.row(i)[56].value,
                                   tb_order_over_time=tabledata.row(i)[57].value,
                                   tb_order_trade_hire_money=fixNullNumber(tabledata.row(i)[58].value),
                                   tb_order_cdcard_hire_money=fixNullNumber(tabledata.row(i)[59].value),
                                   tb_order_return_score=changeStrtoFloat(tabledata.row(i)[60].value),
                                   tb_order_checker=tabledata.row(i)[61].value,
                                   tb_order_printer=tabledata.row(i)[62].value,
                                   tb_order_distributor=tabledata.row(i)[63].value,
                                   tb_order_surveyor=tabledata.row(i)[64].value,
                                   tb_order_packer=tabledata.row(i)[65].value,
                                   tb_order_weighter=tabledata.row(i)[66].value,
                                   tb_order_sender=tabledata.row(i)[67].value,
                                   tb_order_salesman=tabledata.row(i)[68].value,
                                   tb_order_order_date=orderdatequery,
                                   tb_order_store_code=getstorecodebyname(tabledata.row(i)[0].value), tb_order_depart_code=departcode,
                                   tb_order_import_time=currenttime, tb_order_click_farm_flag=1)
            orderobjlist.append(curorder)

        except:
            flag = False
            break

    TbOrder.objects.bulk_create(orderobjlist)
    orderobjlist.clear()
    print('提交数据')
    if flag:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已完成'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()
    else:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已失败'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()

def importstoragedata(tabledata, tableheadrownum, taskobj):
    flag = True
    nrows = tabledata.nrows
    taskfilename = json.loads(taskobj.tb_task_info_content)["savepathname"]
    departcode = taskfilename.split('-')[0].upper()
    importdatestr = taskfilename.split('-')[1].split('.')[0]
    dateobj = datetime.datetime.strptime(importdatestr, "%Y%m%d%H%M%S")
    importdate = dateobj.strftime("%Y-%m-%d")
    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status = '任务进行中'
    taskobj.tb_task_info_starttime = curtime
    taskobj.save()

    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        querycondition = Q()
        querycondition.children.append(('tb_storage_depart_code', departcode))
        querycondition.children.append(('tb_storage_import_date', importdate))
        querycondition.children.append(('tb_storage_product_id', tabledata.row(i)[1].value))
        try:
            updateproduct = TbStorage.objects.get(querycondition)
            updatedata = {}
            updatedata['tb_storage_product_code'] = tabledata.row(i)[0].value
            updatedata['tb_storage_product_id'] = tabledata.row(i)[1].value
            updatedata['tb_storage_product_name'] = tabledata.row(i)[2].value
            updatedata['tb_storage_spec_name'] = tabledata.row(i)[3].value
            updatedata['tb_storage_product_num'] = extractProductNum(tabledata.row(i)[1].value)
            updatedata['tb_storage_catalogue'] = tabledata.row(i)[6].value
            updatedata['tb_storage_actual_stock'] = changeFloattoInt(tabledata.row(i)[7].value)
            updatedata['tb_storage_lock_stock'] = changeFloattoInt(tabledata.row(i)[8].value)
            updatedata['tb_storage_available_stock'] = changeFloattoInt(tabledata.row(i)[9].value)
            updatedata['tb_storage_intransit_stock'] = changeFloattoInt(tabledata.row(i)[10].value)
            updateproduct.__dict__.update(updatedata)
            updateproduct.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStorage.objects.create(tb_storage_product_code=tabledata.row(i)[0].value,
                                     tb_storage_product_id=tabledata.row(i)[1].value,
                                     tb_storage_product_name=tabledata.row(i)[2].value,
                                     tb_storage_spec_name=tabledata.row(i)[3].value,
                                     tb_storage_product_num=extractProductNum(tabledata.row(i)[1].value),
                                     tb_storage_catalogue=tabledata.row(i)[6].value,
                                     tb_storage_actual_stock=changeFloattoInt(tabledata.row(i)[7].value),
                                     tb_storage_lock_stock=changeFloattoInt(tabledata.row(i)[8].value),
                                     tb_storage_available_stock=changeFloattoInt(tabledata.row(i)[9].value),
                                     tb_storage_intransit_stock=changeFloattoInt(tabledata.row(i)[10].value),
                                     tb_storage_import_date=importdate, tb_storage_depart_code=departcode)
        except:
            flag = False
            break

    if flag:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已完成'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()
    else:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已失败'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()


def importstoredata(tabledata, tableheadrownum, taskobj):
    flag = True
    nrows = tabledata.nrows
    taskfilename = json.loads(taskobj.tb_task_info_content)["savepathname"]
    departcode = taskfilename.split('-')[0].upper()
    storecode = taskfilename.split('-')[1].upper()
    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status='任务进行中'
    taskobj.tb_task_info_starttime=curtime
    taskobj.save()

    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        # 店铺推广表
        querystorecostcondition = Q()
        querystorecostcondition.children.append(('tb_store_cost_cal_date', tabledata.row(i)[0].value))
        querystorecostcondition.children.append(('tb_store_cost_store_code', storecode))
        try:
            updatestorecost = TbStoreCost.objects.get(querystorecostcondition)
            updatedata = {}
            updatedata['tb_store_cost_ztc'] = changeStrtoFloat(tabledata.row(i)[77].value)
            updatedata['tb_store_cost_zszw'] = changeStrtoFloat(tabledata.row(i)[78].value)
            updatedata['tb_store_cost_tbk'] = changeStrtoFloat(tabledata.row(i)[79].value)
            updatestorecost.__dict__.update(updatedata)
            updatestorecost.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreCost.objects.create(tb_store_cost_cal_date=tabledata.row(i)[0].value,
                                       tb_store_cost_ztc=changeStrtoFloat(tabledata.row(i)[77].value),
                                       tb_store_cost_zszw=changeStrtoFloat(tabledata.row(i)[78].value),
                                       tb_store_cost_tbk=changeStrtoFloat(tabledata.row(i)[79].value),
                                       tb_store_cost_store_code=storecode, tb_store_cost_depart_code=departcode,
                                       tb_store_cost_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺流量表
        # 店铺流量表-无线端
        querystoreflowcondition1 = Q()
        querystoreflowcondition1.children.append(('tb_store_flow_calDate', tabledata.row(i)[0].value))
        querystoreflowcondition1.children.append(('tb_store_flow_store_code', storecode))
        querystoreflowcondition1.children.append(('tb_store_flow_source', '无线端'))

        try:
            updatestoreflow1 = TbStoreFlow.objects.get(querystoreflowcondition1)
            updatedata = {}
            updatedata['tb_store_flow_visitors'] = changeStrtoInt(tabledata.row(i)[4].value)
            updatedata['tb_store_flow_views'] = changeStrtoInt(tabledata.row(i)[6].value)
            updatedata['tb_store_flow_product_visitors'] = changeStrtoInt(tabledata.row(i)[8].value)
            updatedata['tb_store_flow_product_views'] = changeStrtoInt(tabledata.row(i)[11].value)
            updatedata['tb_store_flow_avg_stoptime'] = changeStrtoFloat(tabledata.row(i)[14].value)
            updatedata['tb_store_flow_jump_percent'] = changeStrtoPercent(tabledata.row(i)[17].value)
            updatedata['tb_store_flow_views_avg'] = changeStrtoFloat(tabledata.row(i)[51].value)
            updatedata['tb_store_flow_visitors_old'] = changeStrtoInt(tabledata.row(i)[66].value)
            updatedata['tb_store_flow_visitors_new'] = changeStrtoInt(tabledata.row(i)[67].value)
            updatestoreflow1.__dict__.update(updatedata)
            updatestoreflow1.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreFlow.objects.create(tb_store_flow_calDate=tabledata.row(i)[0].value,
                                       tb_store_flow_visitors=changeStrtoInt(tabledata.row(i)[4].value),
                                       tb_store_flow_views=changeStrtoInt(tabledata.row(i)[6].value),
                                       tb_store_flow_product_visitors=changeStrtoInt(tabledata.row(i)[8].value),
                                       tb_store_flow_product_views=changeStrtoInt(tabledata.row(i)[11].value),
                                       tb_store_flow_avg_stoptime=changeStrtoFloat(tabledata.row(i)[14].value),
                                       tb_store_flow_jump_percent=changeStrtoPercent(tabledata.row(i)[17].value),
                                       tb_store_flow_views_avg=changeStrtoFloat(tabledata.row(i)[51].value),
                                       tb_store_flow_visitors_old=changeStrtoInt(tabledata.row(i)[66].value),
                                       tb_store_flow_visitors_new=changeStrtoInt(tabledata.row(i)[67].value),
                                       tb_store_flow_source='无线端',
                                       tb_store_flow_store_code=storecode, tb_store_flow_depart_code=departcode,
                                       tb_store_flow_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺流量表-PC端
        querystoreflowcondition2 = Q()
        querystoreflowcondition2.children.append(('tb_store_flow_calDate', tabledata.row(i)[0].value))
        querystoreflowcondition2.children.append(('tb_store_flow_store_code', storecode))
        querystoreflowcondition2.children.append(('tb_store_flow_source', 'PC端'))
        try:
            updatestoreflow2 = TbStoreFlow.objects.get(querystoreflowcondition2)
            updatedata = {}
            updatedata['tb_store_flow_visitors'] = changeStrtoInt(tabledata.row(i)[1].value)
            updatedata['tb_store_flow_views'] = changeStrtoInt(tabledata.row(i)[2].value)
            updatedata['tb_store_flow_product_visitors'] = changeStrtoInt(tabledata.row(i)[9].value)
            updatedata['tb_store_flow_product_views'] = changeStrtoInt(tabledata.row(i)[12].value)
            updatedata['tb_store_flow_avg_stoptime'] = changeStrtoFloat(tabledata.row(i)[15].value)
            updatedata['tb_store_flow_jump_percent'] = changeStrtoPercent(tabledata.row(i)[18].value)
            updatedata['tb_store_flow_views_avg'] = changeStrtoFloat(tabledata.row(i)[50].value)
            updatedata['tb_store_flow_visitors_old'] = changeStrtoInt(tabledata.row(i)[68].value)
            updatedata['tb_store_flow_visitors_new'] = changeStrtoInt(tabledata.row(i)[69].value)
            updatestoreflow2.__dict__.update(updatedata)
            updatestoreflow2.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreFlow.objects.create(tb_store_flow_calDate=tabledata.row(i)[0].value,
                                       tb_store_flow_visitors=changeStrtoInt(tabledata.row(i)[1].value),
                                       tb_store_flow_views=changeStrtoInt(tabledata.row(i)[2].value),
                                       tb_store_flow_product_visitors=changeStrtoInt(tabledata.row(i)[9].value),
                                       tb_store_flow_product_views=changeStrtoInt(tabledata.row(i)[12].value),
                                       tb_store_flow_avg_stoptime=changeStrtoFloat(tabledata.row(i)[15].value),
                                       tb_store_flow_jump_percent=changeStrtoPercent(tabledata.row(i)[18].value),
                                       tb_store_flow_views_avg=changeStrtoFloat(tabledata.row(i)[50].value),
                                       tb_store_flow_visitors_old=changeStrtoInt(tabledata.row(i)[68].value),
                                       tb_store_flow_visitors_new=changeStrtoInt(tabledata.row(i)[69].value),
                                       tb_store_flow_source='PC端', tb_store_flow_store_code=storecode,
                                       tb_store_flow_depart_code=departcode, tb_store_flow_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺流量表-全渠道
        querystoreflowcondition3 = Q()
        querystoreflowcondition3.children.append(('tb_store_flow_calDate', tabledata.row(i)[0].value))
        querystoreflowcondition3.children.append(('tb_store_flow_store_code', storecode))
        querystoreflowcondition3.children.append(('tb_store_flow_source', '全渠道'))
        try:
            updatestoreflow3 = TbStoreFlow.objects.get(querystoreflowcondition3)
            updatedata = {}
            updatedata['tb_store_flow_visitors'] = changeStrtoInt(tabledata.row(i)[3].value)
            updatedata['tb_store_flow_views'] = changeStrtoInt(tabledata.row(i)[5].value)
            updatedata['tb_store_flow_product_visitors'] = changeStrtoInt(tabledata.row(i)[7].value)
            updatedata['tb_store_flow_product_views'] = changeStrtoInt(tabledata.row(i)[10].value)
            updatedata['tb_store_flow_avg_stoptime'] = changeStrtoFloat(tabledata.row(i)[13].value)
            updatedata['tb_store_flow_jump_percent'] = changeStrtoPercent(tabledata.row(i)[16].value)
            updatedata['tb_store_flow_views_avg'] = changeStrtoFloat(tabledata.row(i)[49].value)
            updatedata['tb_store_flow_visitors_old'] = changeStrtoInt(tabledata.row(i)[64].value)
            updatedata['tb_store_flow_visitors_new'] = changeStrtoInt(tabledata.row(i)[65].value)
            updatestoreflow3.__dict__.update(updatedata)
            updatestoreflow3.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreFlow.objects.create(tb_store_flow_calDate=tabledata.row(i)[0].value,
                                       tb_store_flow_visitors=changeStrtoInt(tabledata.row(i)[3].value),
                                       tb_store_flow_views=changeStrtoInt(tabledata.row(i)[5].value),
                                       tb_store_flow_product_visitors=changeStrtoInt(tabledata.row(i)[7].value),
                                       tb_store_flow_product_views=changeStrtoInt(tabledata.row(i)[10].value),
                                       tb_store_flow_avg_stoptime=changeStrtoFloat(tabledata.row(i)[13].value),
                                       tb_store_flow_jump_percent=changeStrtoPercent(tabledata.row(i)[16].value),
                                       tb_store_flow_views_avg=changeStrtoFloat(tabledata.row(i)[49].value),
                                       tb_store_flow_visitors_old=changeStrtoInt(tabledata.row(i)[64].value),
                                       tb_store_flow_visitors_new=changeStrtoInt(tabledata.row(i)[65].value),
                                       tb_store_flow_source='全渠道', tb_store_flow_store_code=storecode,
                                       tb_store_flow_depart_code=departcode, tb_store_flow_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺互动表-无线端
        querystoreinteractioncondition1 = Q()
        querystoreinteractioncondition1.children.append(('tb_store_Interaction_cal_date', tabledata.row(i)[0].value))
        querystoreinteractioncondition1.children.append(('tb_store_Interaction_store_code', storecode))
        querystoreinteractioncondition1.children.append(('tb_store_interaction_store_source', '无线端'))
        try:
            updatestoreinteraction1 = TbStoreInteraction.objects.get(querystoreinteractioncondition1)
            updatedata = {}
            updatedata['tb_store_Interaction_product_collect_buyyers'] = changeStrtoInt(tabledata.row(i)[20].value)
            updatedata['tb_store_Interaction_product_collects'] = changeStrtoInt(tabledata.row(i)[23].value)
            updatedata['tb_store_Interaction_product_adds'] = changeStrtoInt(tabledata.row(i)[26].value)
            updatedata['tb_store_Interaction_product_add_items'] = changeStrtoInt(tabledata.row(i)[72].value)
            updatestoreinteraction1.__dict__.update(updatedata)
            updatestoreinteraction1.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreInteraction.objects.create(tb_store_Interaction_cal_date=tabledata.row(i)[0].value,
                                              tb_store_Interaction_product_collect_buyyers=changeStrtoInt(
                                                  tabledata.row(i)[20].value),
                                              tb_store_Interaction_product_collects=changeStrtoInt(
                                                  tabledata.row(i)[23].value),
                                              tb_store_Interaction_product_adds=changeStrtoInt(
                                                  tabledata.row(i)[26].value),
                                              tb_store_Interaction_product_add_items=changeStrtoInt(
                                                  tabledata.row(i)[72].value), tb_store_interaction_store_source='无线端',
                                              tb_store_Interaction_store_code=storecode,
                                              tb_store_interaction_depart_code=departcode,
                                              tb_store_interaction_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺互动表-PC端
        querystoreinteractioncondition2 = Q()
        querystoreinteractioncondition2.children.append(('tb_store_Interaction_cal_date', tabledata.row(i)[0].value))
        querystoreinteractioncondition2.children.append(('tb_store_Interaction_store_code', storecode))
        querystoreinteractioncondition2.children.append(('tb_store_interaction_store_source', 'PC端'))
        try:
            updatestoreinteraction2 = TbStoreInteraction.objects.get(querystoreinteractioncondition2)
            updatedata = {}
            updatedata['tb_store_Interaction_product_collect_buyyers'] = changeStrtoInt(tabledata.row(i)[21].value)
            updatedata['tb_store_Interaction_product_collects'] = changeStrtoInt(tabledata.row(i)[24].value)
            updatedata['tb_store_Interaction_product_adds'] = changeStrtoInt(tabledata.row(i)[27].value)
            updatedata['tb_store_Interaction_product_add_items'] = changeStrtoInt(tabledata.row(i)[71].value)
            updatestoreinteraction2.__dict__.update(updatedata)
            updatestoreinteraction2.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreInteraction.objects.create(tb_store_Interaction_cal_date=tabledata.row(i)[0].value,
                                              tb_store_Interaction_product_collect_buyyers=changeStrtoInt(
                                                  tabledata.row(i)[21].value),
                                              tb_store_Interaction_product_collects=changeStrtoInt(
                                                  tabledata.row(i)[24].value),
                                              tb_store_Interaction_product_adds=changeStrtoInt(
                                                  tabledata.row(i)[27].value),
                                              tb_store_Interaction_product_add_items=changeStrtoInt(
                                                  tabledata.row(i)[71].value), tb_store_interaction_store_source='PC端',
                                              tb_store_Interaction_store_code=storecode,
                                              tb_store_interaction_depart_code=departcode,
                                              tb_store_interaction_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺互动表-全渠道
        querystoreinteractioncondition3 = Q()
        querystoreinteractioncondition3.children.append(('tb_store_Interaction_cal_date', tabledata.row(i)[0].value))
        querystoreinteractioncondition3.children.append(('tb_store_Interaction_store_code', storecode))
        querystoreinteractioncondition3.children.append(('tb_store_interaction_store_source', '全渠道'))
        try:
            updatestoreinteraction3 = TbStoreInteraction.objects.get(querystoreinteractioncondition3)
            updatedata = {}
            updatedata['tb_store_Interaction_product_collect_buyyers'] = changeStrtoInt(tabledata.row(i)[19].value)
            updatedata['tb_store_Interaction_product_collects'] = changeStrtoInt(tabledata.row(i)[22].value)
            updatedata['tb_store_Interaction_product_adds'] = changeStrtoInt(tabledata.row(i)[25].value)
            updatedata['tb_store_Interaction_product_add_items'] = changeStrtoInt(tabledata.row(i)[70].value)
            updatestoreinteraction3.__dict__.update(updatedata)
            updatestoreinteraction3.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreInteraction.objects.create(tb_store_Interaction_cal_date=tabledata.row(i)[0].value,
                                              tb_store_Interaction_product_collect_buyyers=changeStrtoInt(
                                                  tabledata.row(i)[19].value),
                                              tb_store_Interaction_product_collects=changeStrtoInt(
                                                  tabledata.row(i)[22].value),
                                              tb_store_Interaction_product_adds=changeStrtoInt(
                                                  tabledata.row(i)[25].value),
                                              tb_store_Interaction_product_add_items=changeStrtoInt(
                                                  tabledata.row(i)[70].value), tb_store_interaction_store_source='全渠道',
                                              tb_store_Interaction_store_code=storecode,
                                              tb_store_interaction_depart_code=departcode,
                                              tb_store_interaction_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺物流表
        querystorelogisticcondition = Q()
        querystorelogisticcondition.children.append(('tb_store_logistic_cal_date', tabledata.row(i)[0].value))
        querystorelogisticcondition.children.append(('tb_store_logistic_store_code', storecode))
        try:
            updatestorelogistic = TbStoreLogistic.objects.get(querystorelogisticcondition)
            updatedata = {}
            updatedata['tb_store_logistic_pay_parent_orders'] = changeStrtoInt(tabledata.row(i)[87].value)
            updatedata['tb_store_logistic_pay_child_orders'] = changeStrtoInt(tabledata.row(i)[34].value)
            updatedata['tb_store_logistic_receive_packages'] = changeStrtoInt(tabledata.row(i)[88].value)
            updatedata['tb_store_logistic_send_packages'] = changeStrtoInt(tabledata.row(i)[89].value)
            updatedata['tb_store_logistic_dispatch_packages'] = changeStrtoInt(tabledata.row(i)[90].value)
            updatedata['tb_store_logistic_signed_packages'] = changeStrtoInt(tabledata.row(i)[91].value)
            updatedata['tb_store_logistic_avg_pay_sign_time'] = changeStrtoFloat(tabledata.row(i)[92].value)
            updatestorelogistic.__dict__.update(updatedata)
            updatestorelogistic.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreLogistic.objects.create(tb_store_logistic_cal_date=tabledata.row(i)[0].value,
                                           tb_store_logistic_pay_parent_orders=changeStrtoInt(
                                               tabledata.row(i)[87].value),
                                           tb_store_logistic_pay_child_orders=changeStrtoInt(
                                               tabledata.row(i)[34].value),
                                           tb_store_logistic_receive_packages=changeStrtoInt(
                                               tabledata.row(i)[88].value),
                                           tb_store_logistic_send_packages=changeStrtoInt(tabledata.row(i)[89].value),
                                           tb_store_logistic_dispatch_packages=changeStrtoInt(
                                               tabledata.row(i)[90].value),
                                           tb_store_logistic_signed_packages=changeStrtoInt(tabledata.row(i)[91].value),
                                           tb_store_logistic_avg_pay_sign_time=changeStrtoFloat(
                                               tabledata.row(i)[92].value),
                                           tb_store_logistic_store_code=storecode,
                                           tb_store_logistic_depart_code=departcode,
                                           tb_store_logistic_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺评价表
        querystorereviewcondition = Q()
        querystorereviewcondition.children.append(('tb_store_review_cal_date', tabledata.row(i)[0].value))
        querystorereviewcondition.children.append(('tb_store_review_store_code', storecode))
        try:
            updatestorereview = TbStoreReview.objects.get(querystorereviewcondition)
            updatedata = {}
            updatedata['tb_store_review_reviews'] = changeStrtoInt(tabledata.row(i)[81].value)
            updatedata['tb_store_review_picture_reviews'] = changeStrtoInt(tabledata.row(i)[82].value)
            updatedata['tb_store_review_positive_reviews'] = changeStrtoInt(tabledata.row(i)[83].value)
            updatedata['tb_store_review_critical_reviews'] = changeStrtoInt(tabledata.row(i)[84].value)
            updatedata['tb_store_review_positive_reviews_old'] = changeStrtoInt(tabledata.row(i)[85].value)
            updatedata['tb_store_review_critical_reviews_old'] = changeStrtoInt(tabledata.row(i)[86].value)
            updatedata['tb_store_review_description_score'] = changeStrtoFloat(tabledata.row(i)[93].value)
            updatedata['tb_store_review_logistics_score'] = changeStrtoFloat(tabledata.row(i)[94].value)
            updatedata['tb_store_review_attitude_score'] = changeStrtoFloat(tabledata.row(i)[95].value)
            updatestorereview.__dict__.update(updatedata)
            updatestorereview.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreReview.objects.create(tb_store_review_cal_date=tabledata.row(i)[0].value,
                                         tb_store_review_reviews=changeStrtoInt(tabledata.row(i)[81].value),
                                         tb_store_review_picture_reviews=changeStrtoInt(tabledata.row(i)[82].value),
                                         tb_store_review_positive_reviews=changeStrtoInt(tabledata.row(i)[83].value),
                                         tb_store_review_critical_reviews=changeStrtoInt(tabledata.row(i)[84].value),
                                         tb_store_review_positive_reviews_old=changeStrtoInt(
                                             tabledata.row(i)[85].value),
                                         tb_store_review_critical_reviews_old=changeStrtoInt(
                                             tabledata.row(i)[86].value),
                                         tb_store_review_description_score=changeStrtoFloat(tabledata.row(i)[93].value),
                                         tb_store_review_logistics_score=changeStrtoFloat(tabledata.row(i)[94].value),
                                         tb_store_review_attitude_score=changeStrtoFloat(tabledata.row(i)[95].value),
                                         tb_store_review_store_code=storecode, tb_store_logistic_depart_code=departcode,
                                         tb_store_logistic_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺服务表
        querystoreservicecondition = Q()
        querystoreservicecondition.children.append(('tb_store_service_cal_date', tabledata.row(i)[0].value))
        querystoreservicecondition.children.append(('tb_store_service_store_code', storecode))

        try:
            updatestoreservice = TbStoreService.objects.get(querystoreservicecondition)
            updatedata = {}
            updatedata['tb_store_service_success_return_money'] = changeStrtoFloat(tabledata.row(i)[80].value)
            updatedata['tb_store_service_pay_buyyers_old_money'] = changeStrtoFloat(tabledata.row(i)[76].value)
            updatestoreservice.__dict__.update(updatedata)
            updatestoreservice.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreService.objects.create(tb_store_service_cal_date=tabledata.row(i)[0].value,
                                          tb_store_service_success_return_money=changeStrtoFloat(
                                              tabledata.row(i)[80].value),
                                          tb_store_service_pay_buyyers_old_money=changeStrtoFloat(
                                              tabledata.row(i)[76].value), tb_store_service_store_code=storecode,
                                          tb_store_service_depart_code=departcode,
                                          tb_store_service_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺交易表-无线端
        querystoretradecondition1 = Q()
        querystoretradecondition1.children.append(('tb_store_trade_caldate', tabledata.row(i)[0].value))
        querystoretradecondition1.children.append(('tb_store_trade_store_code', storecode))
        querystoretradecondition1.children.append(('tb_store_trade_store_source', '无线端'))
        try:
            updatestoretrade1 = TbStoreTrade.objects.get(querystoretradecondition1)
            updatedata = {}
            updatedata['tb_store_trade_pay_money'] = changeStrtoFloat(tabledata.row(i)[30].value)
            updatedata['tb_store_trade_pay_buyyers'] = changeStrtoInt(tabledata.row(i)[33].value)
            updatedata['tb_store_trade_pay_childorders'] = changeStrtoInt(tabledata.row(i)[34].value)
            updatedata['tb_store_trade_pay_items'] = changeStrtoInt(tabledata.row(i)[39].value)
            updatedata['tb_store_trade_order_money'] = changeStrtoFloat(tabledata.row(i)[42].value)
            updatedata['tb_store_trade_order_buyyers'] = changeStrtoInt(tabledata.row(i)[45].value)
            updatedata['tb_store_trade_order_items'] = changeStrtoInt(tabledata.row(i)[48].value)
            updatedata['tb_store_trade_buyyers_avg_money'] = changeStrtoFloat(tabledata.row(i)[60].value)
            updatedata['tb_store_trade_uv'] = changeStrtoFloat(tabledata.row(i)[63].value)
            updatedata['tb_store_trade_pay_buyyers_old'] = changeStrtoInt(tabledata.row(i)[75].value)
            updatedata['tb_store_trade_pay_products'] = changeStrtoInt(tabledata.row(i)[101].value)
            updatestoretrade1.__dict__.update(updatedata)
            updatestoretrade1.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreTrade.objects.create(tb_store_trade_caldate=tabledata.row(i)[0].value,
                                        tb_store_trade_pay_money=changeStrtoFloat(tabledata.row(i)[30].value),
                                        tb_store_trade_pay_buyyers=changeStrtoInt(tabledata.row(i)[33].value),
                                        tb_store_trade_pay_childorders=changeStrtoInt(tabledata.row(i)[34].value),
                                        tb_store_trade_pay_items=changeStrtoInt(tabledata.row(i)[39].value),
                                        tb_store_trade_order_money=changeStrtoFloat(tabledata.row(i)[42].value),
                                        tb_store_trade_order_buyyers=changeStrtoInt(tabledata.row(i)[45].value),
                                        tb_store_trade_order_items=changeStrtoInt(tabledata.row(i)[48].value),
                                        tb_store_trade_buyyers_avg_money=changeStrtoFloat(tabledata.row(i)[60].value),
                                        tb_store_trade_uv=changeStrtoFloat(tabledata.row(i)[63].value),
                                        tb_store_trade_pay_buyyers_old=changeStrtoInt(tabledata.row(i)[75].value),
                                        tb_store_trade_pay_products=changeStrtoInt(tabledata.row(i)[101].value),
                                        tb_store_trade_store_source='无线端',
                                        tb_store_trade_store_code=storecode, tb_store_trade_depart_code=departcode,
                                        tb_store_trade_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺交易表-PC端
        querystoretradecondition2 = Q()
        querystoretradecondition2.children.append(('tb_store_trade_caldate', tabledata.row(i)[0].value))
        querystoretradecondition2.children.append(('tb_store_trade_store_code', storecode))
        querystoretradecondition2.children.append(('tb_store_trade_store_source', 'PC端'))
        try:
            updatestoretrade2 = TbStoreTrade.objects.get(querystoretradecondition2)
            updatedata = {}
            updatedata['tb_store_trade_pay_money'] = changeStrtoFloat(tabledata.row(i)[29].value)
            updatedata['tb_store_trade_pay_buyyers'] = changeStrtoInt(tabledata.row(i)[32].value)
            updatedata['tb_store_trade_pay_childorders'] = changeStrtoInt(tabledata.row(i)[35].value)
            updatedata['tb_store_trade_pay_items'] = changeStrtoInt(tabledata.row(i)[38].value)
            updatedata['tb_store_trade_order_money'] = changeStrtoFloat(tabledata.row(i)[41].value)
            updatedata['tb_store_trade_order_buyyers'] = changeStrtoInt(tabledata.row(i)[44].value)
            updatedata['tb_store_trade_order_items'] = changeStrtoInt(tabledata.row(i)[47].value)
            updatedata['tb_store_trade_buyyers_avg_money'] = changeStrtoFloat(tabledata.row(i)[59].value)
            updatedata['tb_store_trade_uv'] = changeStrtoFloat(tabledata.row(i)[62].value)
            updatedata['tb_store_trade_pay_buyyers_old'] = changeStrtoInt(tabledata.row(i)[74].value)
            updatedata['tb_store_trade_pay_products'] = changeStrtoInt(tabledata.row(i)[100].value)
            updatestoretrade2.__dict__.update(updatedata)
            updatestoretrade2.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreTrade.objects.create(tb_store_trade_caldate=tabledata.row(i)[0].value,
                                        tb_store_trade_pay_money=changeStrtoFloat(tabledata.row(i)[29].value),
                                        tb_store_trade_pay_buyyers=changeStrtoInt(tabledata.row(i)[32].value),
                                        tb_store_trade_pay_childorders=changeStrtoInt(tabledata.row(i)[35].value),
                                        tb_store_trade_pay_items=changeStrtoInt(tabledata.row(i)[38].value),
                                        tb_store_trade_order_money=changeStrtoFloat(tabledata.row(i)[41].value),
                                        tb_store_trade_order_buyyers=changeStrtoInt(tabledata.row(i)[44].value),
                                        tb_store_trade_order_items=changeStrtoInt(tabledata.row(i)[47].value),
                                        tb_store_trade_buyyers_avg_money=changeStrtoFloat(tabledata.row(i)[59].value),
                                        tb_store_trade_uv=changeStrtoFloat(tabledata.row(i)[62].value),
                                        tb_store_trade_pay_buyyers_old=changeStrtoInt(tabledata.row(i)[74].value),
                                        tb_store_trade_pay_products=changeStrtoInt(tabledata.row(i)[100].value),
                                        tb_store_trade_store_source='PC端', tb_store_trade_store_code=storecode,
                                        tb_store_trade_depart_code=departcode, tb_store_trade_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺交易表-全渠道
        querystoretradecondition3 = Q()
        querystoretradecondition3.children.append(('tb_store_trade_caldate', tabledata.row(i)[0].value))
        querystoretradecondition3.children.append(('tb_store_trade_store_code', storecode))
        querystoretradecondition3.children.append(('tb_store_trade_store_source', '全渠道'))
        try:
            updatestoretrade3 = TbStoreTrade.objects.get(querystoretradecondition3)
            updatedata = {}
            updatedata['tb_store_trade_pay_money'] = changeStrtoFloat(tabledata.row(i)[28].value)
            updatedata['tb_store_trade_pay_buyyers'] = changeStrtoInt(tabledata.row(i)[31].value)
            updatedata['tb_store_trade_pay_childorders'] = changeStrtoInt(tabledata.row(i)[34].value)
            updatedata['tb_store_trade_pay_items'] = changeStrtoInt(tabledata.row(i)[37].value)
            updatedata['tb_store_trade_order_money'] = changeStrtoFloat(tabledata.row(i)[40].value)
            updatedata['tb_store_trade_order_buyyers'] = changeStrtoInt(tabledata.row(i)[43].value)
            updatedata['tb_store_trade_order_items'] = changeStrtoInt(tabledata.row(i)[46].value)
            updatedata['tb_store_trade_buyyers_avg_money'] = changeStrtoFloat(tabledata.row(i)[58].value)
            updatedata['tb_store_trade_uv'] = changeStrtoFloat(tabledata.row(i)[61].value)
            updatedata['tb_store_trade_pay_buyyers_old'] = changeStrtoInt(tabledata.row(i)[73].value)
            updatedata['tb_store_trade_pay_products'] = changeStrtoInt(tabledata.row(i)[99].value)
            updatestoretrade3.__dict__.update(updatedata)
            updatestoretrade3.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreTrade.objects.create(tb_store_trade_caldate=tabledata.row(i)[0].value,
                                        tb_store_trade_pay_money=changeStrtoFloat(tabledata.row(i)[28].value),
                                        tb_store_trade_pay_buyyers=changeStrtoInt(tabledata.row(i)[31].value),
                                        tb_store_trade_pay_childorders=changeStrtoInt(tabledata.row(i)[34].value),
                                        tb_store_trade_pay_items=changeStrtoInt(tabledata.row(i)[37].value),
                                        tb_store_trade_order_money=changeStrtoFloat(tabledata.row(i)[40].value),
                                        tb_store_trade_order_buyyers=changeStrtoInt(tabledata.row(i)[43].value),
                                        tb_store_trade_order_items=changeStrtoInt(tabledata.row(i)[46].value),
                                        tb_store_trade_buyyers_avg_money=changeStrtoFloat(tabledata.row(i)[58].value),
                                        tb_store_trade_uv=changeStrtoFloat(tabledata.row(i)[61].value),
                                        tb_store_trade_pay_buyyers_old=changeStrtoInt(tabledata.row(i)[73].value),
                                        tb_store_trade_pay_products=changeStrtoInt(tabledata.row(i)[99].value),
                                        tb_store_trade_store_source='全渠道', tb_store_trade_store_code=storecode,
                                        tb_store_trade_depart_code=departcode, tb_store_trade_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺转化表-无线端
        querystoreturncondition1 = Q()
        querystoreturncondition1.children.append(('tb_store_turn_caldate', tabledata.row(i)[0].value))
        querystoreturncondition1.children.append(('tb_store_turn_store_code', storecode))
        querystoreturncondition1.children.append(('tb_store_turn_store_source', '无线端'))
        try:
            updatestoreturn1 = TbStoreTurn.objects.get(querystoreturncondition1)
            updatedata = {}
            updatedata['tb_store_turn_order_turn_percent'] = changeStrtoPercent(tabledata.row(i)[54].value)
            updatedata['tb_store_turn_pay_turn_percent'] = changeStrtoPercent(tabledata.row(i)[57].value)
            updatedata['tb_store_turn_order_pay_turn_percent'] = changeStrtoPercent(tabledata.row(i)[98].value)
            updatedata['tb_store_turn_collect_buyyers'] = changeStrtoInt(tabledata.row(i)[104].value)
            updatestoreturn1.__dict__.update(updatedata)
            updatestoreturn1.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreTurn.objects.create(tb_store_turn_caldate=tabledata.row(i)[0].value,
                                       tb_store_turn_order_turn_percent=changeStrtoPercent(tabledata.row(i)[54].value),
                                       tb_store_turn_pay_turn_percent=changeStrtoPercent(tabledata.row(i)[57].value),
                                       tb_store_turn_order_pay_turn_percent=changeStrtoPercent(
                                           tabledata.row(i)[98].value),
                                       tb_store_turn_collect_buyyers=changeStrtoInt(tabledata.row(i)[104].value),
                                       tb_store_turn_store_source='无线端',
                                       tb_store_turn_store_code=storecode, tb_store_turn_depart_code=departcode,
                                       tb_store_turn_import_time=currenttime)
        except:
            flag = False
            break

        # 店铺转化表 - PC端
        querystoreturncondition2 = Q()
        querystoreturncondition2.children.append(('tb_store_turn_caldate', tabledata.row(i)[0].value))
        querystoreturncondition2.children.append(('tb_store_turn_store_code', storecode))
        querystoreturncondition2.children.append(('tb_store_turn_store_source', 'PC端'))
        try:
            updatestoreturn2 = TbStoreTurn.objects.get(querystoreturncondition2)
            updatedata = {}
            updatedata['tb_store_turn_order_turn_percent'] = changeStrtoPercent(tabledata.row(i)[53].value)
            updatedata['tb_store_turn_pay_turn_percent'] = changeStrtoPercent(tabledata.row(i)[56].value)
            updatedata['tb_store_turn_order_pay_turn_percent'] = changeStrtoPercent(tabledata.row(i)[97].value)
            updatedata['tb_store_turn_collect_buyyers'] = changeStrtoInt(tabledata.row(i)[103].value)
            updatestoreturn2.__dict__.update(updatedata)
            updatestoreturn2.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreTurn.objects.create(tb_store_turn_caldate=tabledata.row(i)[0].value,
                                       tb_store_turn_order_turn_percent=changeStrtoPercent(tabledata.row(i)[53].value),
                                       tb_store_turn_pay_turn_percent=changeStrtoPercent(tabledata.row(i)[56].value),
                                       tb_store_turn_order_pay_turn_percent=changeStrtoPercent(
                                           tabledata.row(i)[97].value),
                                       tb_store_turn_collect_buyyers=changeStrtoInt(tabledata.row(i)[103].value),
                                       tb_store_turn_store_source='PC端',
                                       tb_store_turn_store_code=storecode, tb_store_turn_depart_code=departcode,
                                       tb_store_turn_import_time=currenttime)
        except:
            flag = False

        querystoreturncondition3 = Q()
        querystoreturncondition3.children.append(('tb_store_turn_caldate', tabledata.row(i)[0].value))
        querystoreturncondition3.children.append(('tb_store_turn_store_code', storecode))
        querystoreturncondition3.children.append(('tb_store_turn_store_source', '全渠道'))
        try:
            updatestoreturn3 = TbStoreTurn.objects.get(querystoreturncondition3)
            updatedata = {}
            updatedata['tb_store_turn_order_turn_percent'] = changeStrtoPercent(tabledata.row(i)[52].value)
            updatedata['tb_store_turn_pay_turn_percent'] = changeStrtoPercent(tabledata.row(i)[55].value)
            updatedata['tb_store_turn_order_pay_turn_percent'] = changeStrtoPercent(tabledata.row(i)[96].value)
            updatedata['tb_store_turn_collect_buyyers'] = changeStrtoInt(tabledata.row(i)[102].value)
            updatestoreturn3.__dict__.update(updatedata)
            updatestoreturn3.save()
        except ObjectDoesNotExist:
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            TbStoreTurn.objects.create(tb_store_turn_caldate=tabledata.row(i)[0].value,
                                       tb_store_turn_order_turn_percent=changeStrtoPercent(tabledata.row(i)[52].value),
                                       tb_store_turn_pay_turn_percent=changeStrtoPercent(tabledata.row(i)[55].value),
                                       tb_store_turn_order_pay_turn_percent=changeStrtoPercent(
                                           tabledata.row(i)[96].value),
                                       tb_store_turn_collect_buyyers=changeStrtoInt(tabledata.row(i)[102].value),
                                       tb_store_turn_store_source='全渠道',
                                       tb_store_turn_store_code=storecode, tb_store_turn_depart_code=departcode,
                                       tb_store_turn_import_time=currenttime)
        except:
            flag = False
            break

    if flag:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已完成'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()
    else:
        curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        taskobj.tb_task_info_status='任务已失败'
        taskobj.tb_task_info_endtime=curtime
        taskobj.save()



