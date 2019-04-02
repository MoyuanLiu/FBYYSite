from django.db.models import Q,F,Count
from django.db.models.functions import Substr,Length
from django.db.models.fields import *
from DataManage.models import TbOrder
from ReportManage.models import TbCts
from collections import Counter
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def ctsordercheck(formdata):
    condition = Q()
    if formdata['ctsmakedate'] != '':
        condition.children.append(('tb_order_pay_time__contains', formdata['ctsmakedate'].strftime('%Y/%m/%d')))
    if formdata['ctsmakedepart'] != '':
        condition.children.append(('tb_order_depart_code', formdata['ctsmakedepart']))
    return TbOrder.objects.filter(condition).order_by('-tb_order_pay_time').exists()

def createctsdata(formdata):
    reskeylist=[]
    res={}
    flag=True
    ctscondition = Q()
    if formdata['ctsmakedate'] != '':
        ctscondition.children.append(('tb_cts_cal_date', formdata['ctsmakedate']))
    if formdata['ctsmakedepart'] != '':
        ctscondition.children.append(('tb_cts_cal_depart', formdata['ctsmakedepart']))
    if TbCts.objects.filter(ctscondition).order_by('-tb_cts_cal_date').exists():
        TbCts.objects.filter(ctscondition).order_by('-tb_cts_cal_date').delete()
    condition = Q()
    if formdata['ctsmakedate'] != '':
        condition.children.append(('tb_order_pay_time__contains', formdata['ctsmakedate'].strftime('%Y/%m/%d')))
    if formdata['ctsmakedepart'] != '':
        condition.children.append(('tb_order_depart_code', formdata['ctsmakedepart']))
    condition.children.append(('tb_order_click_farm_flag', 0))
    #res = TbOrder.objects.raw('select tempres.product_num,count(tempres.product_num) as calcount from (select substr(tb_order_product_code,1,length(tb_order_product_code)-1) as product_num from fbyydb.tb_order where tb_order_depart_code=\'%s\' and tb_order_order_date=\'%s\') as tempres group by tempres.product_num ;'%(formdata['ctsmakedepart'],formdata['ctsmakedate'].strftime('%Y/%m/%d')))
    tempres = TbOrder.objects.filter(condition).order_by('-tb_order_pay_time')
    #res = tempres.values('product_num').annotate(cal_count=Count("product_num",output_field=IntegerField())).values('product_num','cal_count')
    #print(tempres)
    #res = Counter(tempres)

    for record in tempres:
        product_num = record.tb_order_product_code
        #print(product_num)
        if product_num[:-1] in reskeylist:
            #print('已存在')
            res[product_num[:-1]]=res[product_num[:-1]]+1
        else:
            reskeylist.append(product_num[:-1])
            res[product_num[:-1]]=1
    reskeylist.clear()
    #print(tempres)
    #print(len(res.keys()))
    tbctslist=[]
    for cts in res.keys():
        curcts = TbCts(tb_cts_product_num=cts,
              tb_cts_sell_count=res[cts],
              tb_cts_cal_date=formdata['ctsmakedate'],
              tb_cts_cal_depart=formdata['ctsmakedepart'])
        #print("%s:%s" %(cts,res[cts]))
        tbctslist.append(curcts)
    res.clear()
    try:
        TbCts.objects.bulk_create(tbctslist)
        tbctslist.clear()
        logger.info('制作公司总销量')
    except Exception as err:
        logger.error(err)
        tbctslist.clear()
        flag = False
    return flag
