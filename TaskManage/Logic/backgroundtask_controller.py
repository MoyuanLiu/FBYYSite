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
import logging
from FBYYSite.settings_production import BASE_DIR


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def expiretaskbyexpiredate():
    logger.info("检查过期任务")
    curdate = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    expiretaskcondition = Q()
    expiretaskcondition.children.append(('tb_task_info_expire_date__lt', curdate))
    expiretasklist = TbTaskInfo.objects.filter(expiretaskcondition)
    for expiretask in expiretasklist:
        expiretask.tb_task_info_status = '任务已过期'
        tasksavefilepath = json.loads(expiretask.tb_task_info_content)["savepath"]
        if os.path.isfile(tasksavefilepath):
            os.remove(tasksavefilepath)
            logger.info("过期任务文件已移除")
            expiretask.save()


def runimporttask(taskobj):
    logger.info("跑导入任务")
    cf = configparser.ConfigParser()
    cf.read(os.path.join(BASE_DIR,"Conf\project.conf"), encoding='UTF-8')
    print(BASE_DIR)
    print(os.path.join(BASE_DIR, "Conf\project.conf"))
    checklistdirlist = []
    taskcode = taskobj.tb_task_info_code
    if taskobj.tb_task_info_code != 'productuploadimporttask':
        logger.info(taskcode)
        taskchecklistconfstr = 'CSD_' + taskcode
        checklistdir = os.path.join(BASE_DIR,cf.get('ImportCheckServicesDir', taskchecklistconfstr))
        checklistdirlist.append(checklistdir)
    else:
        taskchecklistconfstr1 = 'CSD_' + taskcode
        taskchecklistconfstr2 = 'CSD_old' + taskcode
        checklistdir = os.path.join(BASE_DIR,cf.get('ImportCheckServicesDir', taskchecklistconfstr1))
        oldchecklistdir = os.path.join(BASE_DIR,cf.get('ImportCheckServicesDir', taskchecklistconfstr2))
        checklistdirlist.append(checklistdir)
        checklistdirlist.append(oldchecklistdir)
    taskpath = json.loads(taskobj.tb_task_info_content)["savepath"]

    tableheadrownum = int(cf.get('ImportCheckStartRow', 'CSR_' + taskcode))
    if os.path.isfile(taskpath):
        data = xlrd.open_workbook(taskpath)
        table = data.sheets()[0]
        if columncheck(table.row(tableheadrownum), checklistdirlist):
            logger.info('通过校验')
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
        logger.info(readfileaslist(checklistdir))
        logger.info(tableheadlist)
        if operator.eq(readfileaslist(checklistdir), tableheadlist):
            flag = True
    return flag


def importmethoddistribute(taskobj, tabledata, tableheadrownum, ):
    logger.info('分配处理任务')
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
    cf.read(os.path.join(BASE_DIR, "Conf\project.conf"), encoding='UTF-8')
    oldproductchecklistdir = os.path.join(BASE_DIR,cf.get('ImportCheckServicesDir', 'CSD_oldproductuploadimporttask'))
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
    productobjlist = []
    productcaldatestr = tabledata.row((tableheadrownum + 1))[0].value
    if TbProduct.objects.filter(tb_caldate=productcaldatestr).order_by('tb_caldate').exists():
        TbProduct.objects.filter(tb_caldate=productcaldatestr).order_by('tb_caldate').delete()
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        productobj = TbProduct(tb_caldate=tabledata.row(i)[0].value, tb_product_id=tabledata.row(i)[1].value,
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
        productobjlist.append(productobj)
    try:
        TbProduct.objects.bulk_create(productobjlist)
        productobjlist.clear()
        logger.info('提交商品数据')
    except Exception as err:
        logger.error(err)
        productobjlist.clear()
        flag = False
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
    oldproductobjlist = []
    oldproductcaldatestr = tabledata.row((tableheadrownum+1))[0].value
    if TbProduct.objects.filter(tb_caldate=oldproductcaldatestr).order_by('tb_caldate').exists():
        TbProduct.objects.filter(tb_caldate=oldproductcaldatestr).order_by('tb_caldate').delete()
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        oldproductobj = TbProduct(tb_caldate=tabledata.row(i)[0].value, tb_product_id=tabledata.row(i)[1].value,
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
        oldproductobjlist.append(oldproductobj)
    try:
        TbProduct.objects.bulk_create(oldproductobjlist)
        oldproductobjlist.clear()
        logger.info('提交旧版商品数据')
    except Exception as err:
        logger.error(err)
        oldproductobjlist.clear()
        flag = False
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
    #print(storecode)
    curtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    taskobj.tb_task_info_status='任务进行中'
    taskobj.tb_task_info_starttime=curtime
    taskobj.save()
    ztcobjlist = []
    ztccaldatestr = changeExcelDate(tabledata.row((tableheadrownum+1))[0].value)
    if TbZtc.objects.filter(tb_ztc_caldate=ztccaldatestr).order_by('tb_ztc_caldate').exists():
        TbZtc.objects.filter(tb_ztc_caldate=ztccaldatestr).order_by('tb_ztc_caldate').delete()
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        #print(i)
        ztcobj = TbZtc(tb_ztc_caldate=changeExcelDate(tabledata.row(i)[0].value),
                             tb_ztc_plan_name=tabledata.row(i)[1].value,
                             tb_ztc_product_name=tabledata.row(i)[2].value,
                             tb_ztc_product_type=tabledata.row(i)[3].value,
                             tb_ztc_product_id=tabledata.row(i)[4].value,
                             tb_ztc_search_type=tabledata.row(i)[5].value,
                             tb_ztc_traffic_source=tabledata.row(i)[6].value,
                             tb_ztc_impression_count=fixNullNumber(tabledata.row(i)[7].value),
                             tb_ztc_click_count=fixNullNumber(tabledata.row(i)[8].value),
                             tb_ztc_cost=fixNullNumber(tabledata.row(i)[9].value),
                             tb_ztc_click_percent=fixNullNumber(tabledata.row(i)[10].value),
                             tb_ztc_avg_click_cost=fixNullNumber(tabledata.row(i)[11].value),
                             tb_ztc_thousand_impression_cost=fixNullNumber(tabledata.row(i)[12].value),
                             tb_ztc_click_turn_percent=fixNullNumber(tabledata.row(i)[13].value),
                             tb_ztc_direct_deal_money=fixNullNumber(tabledata.row(i)[14].value),
                             tb_ztc_direct_deal_count=fixNullNumber(tabledata.row(i)[15].value),
                             tb_ztc_undirect_deal_money=fixNullNumber(tabledata.row(i)[16].value),
                             tb_ztc_undirect_deal_count=fixNullNumber(tabledata.row(i)[17].value),
                             tb_ztc_deal_money=fixNullNumber(tabledata.row(i)[18].value),
                             tb_ztc_deal_count=fixNullNumber(tabledata.row(i)[19].value),
                             tb_ztc_product_collect_count=fixNullNumber(tabledata.row(i)[20].value),
                             tb_ztc_store_collect_count=fixNullNumber(tabledata.row(i)[21].value),
                             tb_ztc_total_collect_count=fixNullNumber(tabledata.row(i)[22].value),
                             tb_ztc_io_ratio=fixNullNumber(tabledata.row(i)[23].value),
                             tb_ztc_direct_cart_count=fixNullNumber(tabledata.row(i)[24].value),
                             tb_ztc_undirect_cart_count=fixNullNumber(tabledata.row(i)[25].value),
                             tb_ztc_total_cart_count=fixNullNumber(tabledata.row(i)[26].value),
                             tb_ztc_store_code=storecode, tb_ztc_depart_code=departcode,
                             tb_ztc_import_time=currenttime)
        ztcobjlist.append(ztcobj)
    try:
        TbZtc.objects.bulk_create(ztcobjlist)
        ztcobjlist.clear()
        logger.info('提交直通车数据')
    except Exception as err:
        #print(err)
        logger.error(err)
        ztcobjlist.clear()
        flag = False
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
    orderdate = getdatestr(tabledata.row((tableheadrownum + 1))[53].value)
    if TbOrder.objects.filter(tb_order_order_date=orderdate).order_by('tb_order_order_date').exists():
        TbOrder.objects.filter(tb_order_order_date=orderdate).order_by('tb_order_order_date').delete()
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
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
                               tb_order_order_date=getdatestr(tabledata.row(i)[53].value),
                               tb_order_store_code=getstorecodebyname(tabledata.row(i)[0].value), tb_order_depart_code=departcode,
                               tb_order_import_time=currenttime)
            orderobjlist.append(curorder)
        except Exception as err:
            logger.error(err)
            flag = False
            break
    try:
        TbOrder.objects.bulk_create(orderobjlist)
        orderobjlist.clear()
        logger.info('提交万里牛订单数据')
    except Exception as err:
        logger.error(err)
        orderobjlist.clear()
        flag = False
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
    orderidlist = []
    orderdate = getdatestr(tabledata.row((tableheadrownum+1))[53].value)
    if TbOrder.objects.filter(tb_order_order_date=orderdate).order_by('tb_order_order_date').exists():
        for i in range(nrows):
            if i <= tableheadrownum:
                continue
            orderidlist.append(tabledata.row(i)[1].value)
        querycondition = Q()
        querycondition.children.append(('tb_order_order_date', orderdate))
        querycondition.children.append(('tb_order_id__in', orderidlist))
        try:
            TbOrder.objects.filter(querycondition).update(tb_order_click_farm_flag=1)
            logger.info('更新万里牛刷单数据')
        except Exception as err:
            logger.error(err)
            flag = False

    else:
        for i in range(nrows):
            if i <= tableheadrownum:
                continue
            currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            curorder = TbOrder(tb_order_store_name=fixStoreName(tabledata.row(i)[0].value),
                               tb_order_id=tabledata.row(i)[1].value, tb_order_sys_id=tabledata.row(i)[2].value,
                               tb_order_mark=tabledata.row(i)[3].value,
                               tb_order_actual_pay_count=fixNullNumber(tabledata.row(i)[4].value),
                               tb_order_benifit_count=fixNullNumber(tabledata.row(i)[5].value),
                               tb_order_storage_code=tabledata.row(i)[6].value,
                               tb_order_storage_name=tabledata.row(i)[7].value,
                               tb_order_buyyer_review=tabledata.row(i)[8].value,
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
                               tb_order_receiver_name=tabledata.row(i)[45].value,
                               tb_order_idcard_num=tabledata.row(i)[46].value,
                               tb_order_receiver_tel=tabledata.row(i)[47].value,
                               tb_order_receiver_province=tabledata.row(i)[48].value,
                               tb_order_receiver_city=tabledata.row(i)[49].value,
                               tb_order_receiver_county=tabledata.row(i)[50].value,
                               tb_order_receiver_detail_address=tabledata.row(i)[51].value,
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
                               tb_order_order_date=getdatestr(tabledata.row(i)[53].value),
                               tb_order_store_code=getstorecodebyname(tabledata.row(i)[0].value),
                               tb_order_depart_code=departcode,
                               tb_order_import_time=currenttime, tb_order_click_farm_flag=1)
            orderobjlist.append(curorder)
        try:
            TbOrder.objects.bulk_create(orderobjlist)
            orderobjlist.clear()
            logger.info('提交万里牛刷单数据')
        except Exception as err:
            logger.error(err)
            orderobjlist.clear()
            flag=False

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
    storageobjlist = []
    if TbStorage.objects.filter(tb_storage_import_date=importdate).order_by('tb_storage_import_date').exists():
        TbStorage.objects.filter(tb_storage_import_date=importdate).order_by('tb_storage_import_date').delete()
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        storageobj = TbStorage(tb_storage_product_code=tabledata.row(i)[0].value,
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
        storageobjlist.append(storageobj)
    try:
        TbStorage.objects.bulk_create(storageobjlist)
        storageobjlist.clear()
        logger.info('提交万里牛库存数据')
    except Exception as err:
        logger.error(err)
        storageobjlist.clear()
        flag = False

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
    storecostobjlist = []
    storeflowobjlist = []
    storeinteractionobjlist = []
    storelogisticobjlist = []
    storereviewobjlist = []
    storeserviceobjlist = []
    storetradeobjlist = []
    storeturnobjlist = []
    caldatestr = tabledata.row((tableheadrownum+1))[0].value
    if TbStoreCost.objects.filter(tb_store_cost_cal_date=caldatestr).order_by('tb_store_cost_cal_date').exists():
        TbStoreCost.objects.filter(tb_store_cost_cal_date=caldatestr).order_by('tb_store_cost_cal_date').delete()
    if TbStoreFlow.objects.filter(tb_store_flow_calDate=caldatestr).order_by('tb_store_flow_calDate').exists():
        TbStoreFlow.objects.filter(tb_store_flow_calDate=caldatestr).order_by('tb_store_flow_calDate').delete()
    if TbStoreInteraction.objects.filter(tb_store_Interaction_cal_date=caldatestr).order_by('tb_store_Interaction_cal_date').exists():
        TbStoreInteraction.objects.filter(tb_store_Interaction_cal_date=caldatestr).order_by('tb_store_Interaction_cal_date').delete()
    if TbStoreLogistic.objects.filter(tb_store_logistic_cal_date=caldatestr).order_by('tb_store_logistic_cal_date').exists():
        TbStoreLogistic.objects.filter(tb_store_logistic_cal_date=caldatestr).order_by('tb_store_logistic_cal_date').delete()
    if TbStoreReview.objects.filter(tb_store_review_cal_date=caldatestr).order_by('tb_store_review_cal_date').exists():
        TbStoreReview.objects.filter(tb_store_review_cal_date=caldatestr).order_by('tb_store_review_cal_date').delete()
    if TbStoreService.objects.filter(tb_store_service_cal_date=caldatestr).order_by('tb_store_service_cal_date').exists():
        TbStoreService.objects.filter(tb_store_service_cal_date=caldatestr).order_by('tb_store_service_cal_date').delete()
    if TbStoreTrade.objects.filter(tb_store_trade_caldate=caldatestr).order_by('tb_store_trade_caldate').exists():
        TbStoreTrade.objects.filter(tb_store_trade_caldate=caldatestr).order_by('tb_store_trade_caldate').delete()
    if TbStoreTurn.objects.filter(tb_store_turn_caldate=caldatestr).order_by('tb_store_turn_caldate').exists():
        TbStoreTurn.objects.filter(tb_store_turn_caldate=caldatestr).order_by('tb_store_turn_caldate').delete()
    for i in range(nrows):
        if i <= tableheadrownum:
            continue
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storecostobj = TbStoreCost(tb_store_cost_cal_date=tabledata.row(i)[0].value,
                                   tb_store_cost_ztc=changeStrtoFloat(tabledata.row(i)[77].value),
                                   tb_store_cost_zszw=changeStrtoFloat(tabledata.row(i)[78].value),
                                   tb_store_cost_tbk=changeStrtoFloat(tabledata.row(i)[79].value),
                                   tb_store_cost_store_code=storecode, tb_store_cost_depart_code=departcode,
                                   tb_store_cost_import_time=currenttime)
        storecostobjlist.append(storecostobj)

        # 店铺流量表
        # 店铺流量表-无线端
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeflowobj1 = TbStoreFlow(tb_store_flow_calDate=tabledata.row(i)[0].value,
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
        storeflowobjlist.append(storeflowobj1)

        # 店铺流量表-PC端
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeflowobj2 = TbStoreFlow(tb_store_flow_calDate=tabledata.row(i)[0].value,
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
        storeflowobjlist.append(storeflowobj2)

        # 店铺流量表-全渠道
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeflowobj3 = TbStoreFlow(tb_store_flow_calDate=tabledata.row(i)[0].value,
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
        storeflowobjlist.append(storeflowobj3)

        # 店铺互动表-无线端
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeinteractionobj1 = TbStoreInteraction(tb_store_Interaction_cal_date=tabledata.row(i)[0].value,
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
        storeinteractionobjlist.append(storeinteractionobj1)

        # 店铺互动表-PC端

        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeinteractionobj2 = TbStoreInteraction(tb_store_Interaction_cal_date=tabledata.row(i)[0].value,
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
        storeinteractionobjlist.append(storeinteractionobj2)

        # 店铺互动表-全渠道
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeinteractionobj3 = TbStoreInteraction(tb_store_Interaction_cal_date=tabledata.row(i)[0].value,
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
        storeinteractionobjlist.append(storeinteractionobj3)

        # 店铺物流表
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storelogisticobj = TbStoreLogistic(tb_store_logistic_cal_date=tabledata.row(i)[0].value,
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
        storelogisticobjlist.append(storelogisticobj)

        # 店铺评价表
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storereviewobj = TbStoreReview(tb_store_review_cal_date=tabledata.row(i)[0].value,
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
        storereviewobjlist.append(storereviewobj)

        # 店铺服务表
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeserviceobj = TbStoreService(tb_store_service_cal_date=tabledata.row(i)[0].value,
                                      tb_store_service_success_return_money=changeStrtoFloat(
                                          tabledata.row(i)[80].value),
                                      tb_store_service_pay_buyyers_old_money=changeStrtoFloat(
                                          tabledata.row(i)[76].value), tb_store_service_store_code=storecode,
                                      tb_store_service_depart_code=departcode,
                                      tb_store_service_import_time=currenttime)
        storeserviceobjlist.append(storeserviceobj)

        # 店铺交易表-无线端
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storetradeobj1 = TbStoreTrade(tb_store_trade_caldate=tabledata.row(i)[0].value,
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
        storetradeobjlist.append(storetradeobj1)

        # 店铺交易表-PC端

        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storetradeobj2 = TbStoreTrade(tb_store_trade_caldate=tabledata.row(i)[0].value,
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
        storetradeobjlist.append(storetradeobj2)
        # 店铺交易表-全渠道
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storetradeobj3 = TbStoreTrade(tb_store_trade_caldate=tabledata.row(i)[0].value,
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
        storetradeobjlist.append(storetradeobj3)

        # 店铺转化表-无线端
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeturnobj1 = TbStoreTurn(tb_store_turn_caldate=tabledata.row(i)[0].value,
                                   tb_store_turn_order_turn_percent=changeStrtoPercent(tabledata.row(i)[54].value),
                                   tb_store_turn_pay_turn_percent=changeStrtoPercent(tabledata.row(i)[57].value),
                                   tb_store_turn_order_pay_turn_percent=changeStrtoPercent(
                                       tabledata.row(i)[98].value),
                                   tb_store_turn_collect_buyyers=changeStrtoInt(tabledata.row(i)[104].value),
                                   tb_store_turn_store_source='无线端',
                                   tb_store_turn_store_code=storecode, tb_store_turn_depart_code=departcode,
                                   tb_store_turn_import_time=currenttime)
        storeturnobjlist.append(storeturnobj1)
        # 店铺转化表 - PC端
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeturnobj2 = TbStoreTurn(tb_store_turn_caldate=tabledata.row(i)[0].value,
                                   tb_store_turn_order_turn_percent=changeStrtoPercent(tabledata.row(i)[53].value),
                                   tb_store_turn_pay_turn_percent=changeStrtoPercent(tabledata.row(i)[56].value),
                                   tb_store_turn_order_pay_turn_percent=changeStrtoPercent(
                                       tabledata.row(i)[97].value),
                                   tb_store_turn_collect_buyyers=changeStrtoInt(tabledata.row(i)[103].value),
                                   tb_store_turn_store_source='PC端',
                                   tb_store_turn_store_code=storecode, tb_store_turn_depart_code=departcode,
                                   tb_store_turn_import_time=currenttime)
        storeturnobjlist.append(storeturnobj2)

        # 店铺转化表 - 全渠道
        currenttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        storeturnobj3 = TbStoreTurn(tb_store_turn_caldate=tabledata.row(i)[0].value,
                                   tb_store_turn_order_turn_percent=changeStrtoPercent(tabledata.row(i)[52].value),
                                   tb_store_turn_pay_turn_percent=changeStrtoPercent(tabledata.row(i)[55].value),
                                   tb_store_turn_order_pay_turn_percent=changeStrtoPercent(
                                       tabledata.row(i)[96].value),
                                   tb_store_turn_collect_buyyers=changeStrtoInt(tabledata.row(i)[102].value),
                                   tb_store_turn_store_source='全渠道',
                                   tb_store_turn_store_code=storecode, tb_store_turn_depart_code=departcode,
                                   tb_store_turn_import_time=currenttime)
        storeturnobjlist.append(storeturnobj3)
    try:
        TbStoreCost.objects.bulk_create(storecostobjlist)
        TbStoreFlow.objects.bulk_create(storeflowobjlist)
        TbStoreInteraction.objects.bulk_create(storeinteractionobjlist)
        TbStoreLogistic.objects.bulk_create(storelogisticobjlist)
        TbStoreReview.objects.bulk_create(storereviewobjlist)
        TbStoreService.objects.bulk_create(storeserviceobjlist)
        TbStoreTrade.objects.bulk_create(storetradeobjlist)
        TbStoreTurn.objects.bulk_create(storeturnobjlist)

        storecostobjlist.clear()
        storeflowobjlist.clear()
        storeinteractionobjlist.clear()
        storelogisticobjlist.clear()
        storereviewobjlist.clear()
        storeserviceobjlist.clear()
        storetradeobjlist.clear()
        storeturnobjlist.clear()

        logger.info('提交店铺数据')
    except Exception as err:
        logger.error(err)
        storecostobjlist.clear()
        storeflowobjlist.clear()
        storeinteractionobjlist.clear()
        storelogisticobjlist.clear()
        storereviewobjlist.clear()
        storeserviceobjlist.clear()
        storetradeobjlist.clear()
        storeturnobjlist.clear()
        flag = False

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



