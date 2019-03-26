# -*- coding: UTF-8 -*-
from DataManage.models import *
from django.db.models import Q,F
from Utils.DateTimeUtil import *
import json
from django.core import serializers
import time
import string

def get_store_cost_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_cost_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_cost_store_code__in', storecodelist))
    if condition.children:
        return TbStoreCost.objects.filter(condition)
    else:
        return TbStoreCost.objects.all()

def get_store_flow_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_flow_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_flow_store_code__in', storecodelist))
    if condition.children:
        return TbStoreFlow.objects.filter(condition)
    else:
        return TbStoreFlow.objects.all()

def get_store_interaction_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_interaction_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_interaction_store_code__in', storecodelist))
    if condition.children:
        return TbStoreInteraction.objects.filter(condition)
    else:
        return TbStoreInteraction.objects.all()

def get_store_logistic_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_logistic_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_logistic_store_code__in', storecodelist))
    if condition.children:
        return TbStoreLogistic.objects.filter(condition)
    else:
        return TbStoreLogistic.objects.all()

def get_store_review_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_review_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_review_store_code__in', storecodelist))
    if condition.children:
        return TbStoreReview.objects.filter(condition)
    else:
        return TbStoreReview.objects.all()

def get_store_service_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_service_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_service_store_code__in', storecodelist))
    if condition.children:
        return TbStoreService.objects.filter(condition)
    else:
        return TbStoreService.objects.all()

def get_store_trade_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_trade_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_trade_store_code__in', storecodelist))
    if condition.children:
        return TbStoreTrade.objects.filter(condition)
    else:
        return TbStoreTrade.objects.all()

def get_store_turn_data_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_store_turn_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_store_turn_store_code__in', storecodelist))
    if condition.children:
        return TbStoreTurn.objects.filter(condition)
    else:
        return TbStoreTurn.objects.all()

def storecost_query(formdata):
    condition = Q()
    if formdata['storecostimportdateflag']:
        condition.children.append(('tb_store_cost_import_time__contains', formdata['storecostimportdate'].strftime('%Y/%m/%d')))
    if formdata['storecostcaldateflag']:
        condition.children.append(('tb_store_cost_cal_date__contains', formdata['storecostcaldate'].strftime('%Y-%m-%d')))
    if formdata['querystorecostdepart'] != '':
        condition.children.append(('tb_store_cost_depart_code', formdata['querystorecostdepart']))
    if formdata['querystorecoststore'] != '':
        condition.children.append(('tb_store_cost_store_code', formdata['querystorecoststore']))
    query_storecostlist = TbStoreCost.objects.filter(condition)
    return query_storecostlist

def storeflow_query(formdata):
    condition = Q()
    if formdata['storeflowimportdateflag'] and formdata['storeflowimportdate']:
        condition.children.append(('tb_store_flow_import_time__contains', formdata['storeflowimportdate'].strftime('%Y/%m/%d')))
    if formdata['storeflowcaldateflag'] and formdata['storeflowcaldate']:
        condition.children.append(('tb_store_flow_caldate__contains', formdata['storeflowcaldate'].strftime('%Y-%m-%d')))
    if formdata['storeflowstoresourceflag'] and formdata['storeflowstoresource']:
        condition.children.append(('tb_store_flow_source', formdata['storeflowstoresource']))
    if formdata['querystoreflowdepart'] != '':
        condition.children.append(('tb_store_flow_depart_code', formdata['querystoreflowdepart']))
    if formdata['querystoreflowstore'] != '':
        condition.children.append(('tb_store_flow_store_code', formdata['querystoreflowstore']))
    query_storeflowlist = TbStoreFlow.objects.filter(condition)
    return query_storeflowlist

def storeinteraction_query(formdata):
    condition = Q()
    if formdata['storeinteractionimportdateflag'] and formdata['storeinteractionimportdate']:
        condition.children.append(('tb_store_interaction_import_time__contains', formdata['storeinteractionimportdate'].strftime('%Y/%m/%d')))
    if formdata['storeinteractioncaldateflag'] and formdata['storeinteractioncaldate']:
        condition.children.append(('tb_store_interaction_cal_date__contains', formdata['storeinteractioncaldate'].strftime('%Y-%m-%d')))
    if formdata['storeinteractionstoresourceflag'] and formdata['storeinteractionstoresource']:
        condition.children.append(('tb_store_interaction_store_source', formdata['storeinteractionstoresource']))
    if formdata['querystoreinteractiondepart'] != '':
        condition.children.append(('tb_store_interaction_depart_code', formdata['querystoreinteractiondepart']))
    if formdata['querystoreinteractionstore'] != '':
        condition.children.append(('tb_store_interaction_store_code', formdata['querystoreinteractionstore']))
    query_storeinteractionlist = TbStoreInteraction.objects.filter(condition)
    return query_storeinteractionlist

def storelogistic_query(formdata):
    condition = Q()
    if formdata['storelogisticimportdateflag'] and formdata['storelogisticimportdate']:
        condition.children.append(('tb_store_logistic_import_time__contains', formdata['storelogisticimportdate'].strftime('%Y/%m/%d')))
    if formdata['storelogisticcaldateflag'] and formdata['storelogisticcaldate']:
        condition.children.append(('tb_store_logistic_cal_date__contains', formdata['storelogisticcaldate'].strftime('%Y-%m-%d')))
    if formdata['querystorelogisticdepart'] != '':
        condition.children.append(('tb_store_logistic_depart_code', formdata['querystorelogisticdepart']))
    if formdata['querystorelogisticstore'] != '':
        condition.children.append(('tb_store_logistic_store_code', formdata['querystorelogisticstore']))
    query_storelogisticlist = TbStoreLogistic.objects.filter(condition)
    return query_storelogisticlist

def storereview_query(formdata):
    condition = Q()
    if formdata['storereviewimportdateflag'] and formdata['storereviewimportdate']:
        condition.children.append(('tb_store_review_import_time__contains', formdata['storereviewimportdate'].strftime('%Y/%m/%d')))
    if formdata['storereviewcaldateflag'] and formdata['storereviewcaldate']:
        condition.children.append(('tb_store_review_cal_date__contains', formdata['storereviewcaldate'].strftime('%Y-%m-%d')))
    if formdata['querystorereviewdepart'] != '':
        condition.children.append(('tb_store_review_depart_code', formdata['querystorereviewdepart']))
    if formdata['querystorereviewstore'] != '':
        condition.children.append(('tb_store_review_store_code', formdata['querystorereviewstore']))
    query_storereviewlist = TbStoreReview.objects.filter(condition)
    return query_storereviewlist

def storeservice_query(formdata):
    condition = Q()
    if formdata['storeserviceimportdateflag'] and formdata['storeserviceimportdate']:
        condition.children.append(('tb_store_service_import_time__contains', formdata['storeserviceimportdate'].strftime('%Y/%m/%d')))
    if formdata['storeservicecaldateflag'] and formdata['storeservicecaldate']:
        condition.children.append(('tb_store_service_cal_date__contains', formdata['storeservicecaldate'].strftime('%Y-%m-%d')))
    if formdata['querystoreservicedepart'] != '':
        condition.children.append(('tb_store_service_depart_code', formdata['querystoreservicedepart']))
    if formdata['querystoreservicestore'] != '':
        condition.children.append(('tb_store_service_store_code', formdata['querystoreservicestore']))
    query_storeservicelist = TbStoreService.objects.filter(condition)
    return query_storeservicelist

def storetrade_query(formdata):
    condition = Q()
    if formdata['storetradeimportdateflag'] and formdata['storetradeimportdate']:
        condition.children.append(('tb_store_trade_import_time__contains', formdata['storetradeimportdate'].strftime('%Y/%m/%d')))
    if formdata['storetradecaldateflag'] and formdata['storetradecaldate']:
        condition.children.append(('tb_store_trade_caldate__contains', formdata['storetradecaldate'].strftime('%Y-%m-%d')))
    if formdata['storetradestoresourceflag'] and formdata['storetradestoresource']:
        condition.children.append(('tb_store_trade_store_source', formdata['storetradestoresource']))
    if formdata['querystoretradedepart'] != '':
        condition.children.append(('tb_store_trade_depart_code', formdata['querystoretradedepart']))
    if formdata['querystoretradestore'] != '':
        condition.children.append(('tb_store_trade_store_code', formdata['querystoretradestore']))
    query_storetradelist = TbStoreTrade.objects.filter(condition)
    return query_storetradelist

def storeturn_query(formdata):
    condition = Q()
    if formdata['storeturnimportdateflag'] and formdata['storeturnimportdate']:
        condition.children.append(('tb_store_turn_import_time__contains', formdata['storeturnimportdate'].strftime('%Y/%m/%d')))
    if formdata['storeturncaldateflag'] and formdata['storeturncaldate']:
        condition.children.append(('tb_store_turn_caldate__contains', formdata['storeturncaldate'].strftime('%Y-%m-%d')))
    if formdata['storeturnstoresourceflag'] and formdata['storeturnstoresource']:
        condition.children.append(('tb_store_turn_store_source', formdata['storeturnstoresource']))
    if formdata['querystoreturndepart'] != '':
        condition.children.append(('tb_store_turn_depart_code', formdata['querystoreturndepart']))
    if formdata['querystoreturnstore'] != '':
        condition.children.append(('tb_store_turn_store_code', formdata['querystoreturnstore']))
    query_storeturnlist = TbStoreTurn.objects.filter(condition)
    return query_storeturnlist

def createstoreimporttask(useraccount,taskcontentdict):
    createtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    expiredate = get_day_of_today(7).strftime('%Y/%m/%d')
    userid = TbUserInfo.objects.get_user_by_account(useraccount).idtb_user_info
    taskcontentstr = json.dumps(taskcontentdict, ensure_ascii=False).encode('utf-8').decode('utf-8')
    TbTaskInfo.objects.newtask('店铺数据上传导入任务', '上传', taskcontentstr, userid, createtime, '任务未完成', expiredate,'storeuploadimporttask')