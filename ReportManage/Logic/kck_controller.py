from SiteLogin.models import TbUserInfo
from ReportManage.models import *
from django.db.models import Q,F
import time
import os
import configparser
from FBYYSite.settings_production import BASE_DIR


def get_kcklist_by_permission(querypermissiondict):
    departcodelist = []
    storecodelist = []
    for departobj in querypermissiondict['departlist']:
        departcodelist.append(departobj.tb_department_info_code)
    for storeobj in querypermissiondict['storelist']:
        storecodelist.append(storeobj.tb_store_code)
    condition = Q()
    if departcodelist:
        condition.children.append(('tb_kck_depart_code__in', departcodelist))
    if storecodelist:
        condition.children.append(('tb_kck_store_code__in', storecodelist))
    if condition.children:
        return TbKck.objects.filter(condition)
    else:
        return TbKck.objects.all()

def kck_add(formdata):
    TbKck.objects.create(tb_kck_product_id=formdata['kckproductid'],
                         tb_kck_product_color_num=formdata['kckproductcolornum'],
                         tb_kck_product_category=formdata['kckproductcategory'],
                         tb_kck_product_shelf_date=formdata['kckshelfdate'],
                         tb_kck_store_code=formdata['kckselstore'],
                         tb_kck_depart_code=formdata['kckseldepart'],
                         )

def kck_info_list(kcklist):
    cf = configparser.ConfigParser()
    cf.read(os.path.join(BASE_DIR, "Conf\project.conf"), encoding='UTF-8')
    link_prefix_tm = cf.get('LinkPrefix', 'LP_TM')
    link_prefix_tb = cf.get('LinkPrefix', 'LP_TB')
    kckinfolist=[]
    for kck in kcklist:
        kckinfodict={}
        kckinfodict['idtb_kck']=kck.idtb_kck
        kckinfodict['tb_kck_product_id'] = kck.tb_kck_product_id
        kckinfodict['tb_kck_product_color_num'] = kck.tb_kck_product_color_num
        kckinfodict['tb_kck_product_category'] = kck.tb_kck_product_category
        kckinfodict['tb_kck_product_shelf_date'] = kck.tb_kck_product_shelf_date
        kckinfodict['tb_kck_store_code'] = kck.tb_kck_store_code
        kckinfodict['tb_kck_depart_code'] = kck.tb_kck_depart_code
        if kck.tb_kck_store_code=='TM':
            kckinfodict['tb_kck_product_link']=link_prefix_tm+kck.tb_kck_product_id
        else:
            kckinfodict['tb_kck_product_link'] = link_prefix_tb + kck.tb_kck_product_id
        kckinfolist.append(kckinfodict)
    return kckinfolist

def update_kck_edit(formdata):
    update_kck = TbKck.objects.get(idtb_kck=int(formdata['kckid']))
    update_kck.tb_kck_product_id = formdata['kckproductid']
    update_kck.tb_kck_product_color_num = formdata['kckproductcolornum']
    update_kck.tb_kck_product_category = formdata['kckproductcategory']
    update_kck.tb_kck_product_shelf_date = formdata['kckshelfdate']
    update_kck.tb_kck_depart_code = formdata['kckseldepart']
    update_kck.tb_kck_store_code = formdata['kckselstore']
    update_kck.save()

def kck_del(kckid):
    deluser = TbKck.objects.get(idtb_kck=int(kckid))
    deluser.delete()

def kck_query(formdata):
    condition = Q()
    if formdata['kckshelfdateflag']:
        condition.children.append(('tb_kck_product_shelf_date', formdata['kckshelfdate'].strftime('%Y-%m-%d')))
    if formdata['kckproductid'] != '':
        condition.children.append(('tb_kck_product_id', formdata['kckproductid']))
    if formdata['kckproductcolornum'] != '':
        condition.children.append(('tb_kck_product_color_num', formdata['kckproductcolornum']))
    if formdata['kckproductcategory'] != '':
        condition.children.append(('tb_kck_product_category', formdata['kckproductcategory']))
    if formdata['kckseldepart'] != '':
        condition.children.append(('tb_kck_depart_code', formdata['kckseldepart']))
    if formdata['kckselstore'] != '':
        condition.children.append(('tb_kck_store_code', formdata['kckselstore']))
    query_kcklist = TbKck.objects.filter(condition)
    return query_kcklist

def get_kck_data_by_permission(querypermissiondict):
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
        return TbKck.objects.filter(condition)
    else:
        return TbKck.objects.all()