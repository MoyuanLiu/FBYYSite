# -*- coding: UTF-8 -*-
from django.db import models

from SiteLogin.models import *

# Create your models here.

class TbProduct(models.Model):
    idtb_product = models.AutoField(primary_key=True)
    tb_caldate = models.CharField(max_length=45)
    tb_product_id = models.CharField(max_length=45)
    tb_product_name = models.CharField(max_length=200)
    tb_product_num = models.CharField(max_length=45)
    tb_product_product_status = models.CharField(max_length=45, blank=True, null=True)
    tb_product_product_tag = models.CharField(max_length=45, blank=True, null=True)
    tb_product_visitors = models.IntegerField()
    tb_product_views = models.IntegerField()
    tb_avg_stoptime = models.FloatField()
    tb_detail_page_jump_percent = models.FloatField()
    tb_product_collects = models.IntegerField()
    tb_product_join_items = models.IntegerField()
    tb_product_joins = models.IntegerField(blank=True, null=True)
    tb_product_order_buyyers = models.IntegerField(blank=True, null=True)
    tb_product_buy_order_items = models.IntegerField(blank=True, null=True)
    tb_product_buy_order_money = models.FloatField(blank=True, null=True)
    tb_product_order_converse_percent = models.FloatField(blank=True, null=True)
    tb_product_payers = models.IntegerField(blank=True, null=True)
    tb_product_pay_items = models.IntegerField(blank=True, null=True)
    tb_product_pay_money = models.FloatField(blank=True, null=True)
    tb_product_pay_converse_percent = models.FloatField(blank=True, null=True)
    tb_product_new_payyers = models.IntegerField(blank=True, null=True)
    tb_product_old_payyers = models.IntegerField(blank=True, null=True)
    tb_product_old_payyer_money = models.FloatField(blank=True, null=True)
    tb_product_juhuasuan_money = models.FloatField(blank=True, null=True)
    tb_product_avg_value_visitors = models.FloatField(blank=True, null=True)
    tb_product_sell_return_money = models.FloatField(blank=True, null=True)
    tb_product_compare_score = models.FloatField(blank=True, null=True)
    tb_product_count_year_money = models.FloatField(blank=True, null=True)
    tb_product_count_month_money = models.FloatField(blank=True, null=True)
    tb_product_count_month_items = models.IntegerField(blank=True, null=True)
    tb_product_store_id = models.CharField(max_length=45, blank=True, null=True)
    tb_product_search_into_pay_percent = models.FloatField(blank=True, null=True)
    tb_product_search_into_visitors = models.IntegerField(blank=True, null=True)
    tb_product_search_into_pay_buyyers = models.IntegerField(blank=True, null=True)
    tb_product_depart_id = models.CharField(max_length=45, blank=True, null=True)
    tb_product_import_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tb_product'

class TbTaskInfoManager(models.Manager):
    def newtask(self,taskname,tasktype,taskcontent,taskuserid,taskcreatetime,taskstatus,taskexpiredate):
        self.create(tb_task_info_name=taskname,tb_task_info_type=tasktype,tb_task_info_content=taskcontent,tb_task_info_user_id=taskuserid,tb_task_info_createtime=taskcreatetime,tb_task_info_status=taskstatus,tb_task_info_expire_date=taskexpiredate,tb_task_info_delflag=0)

class TbTaskInfo(models.Model):
    idtb_task_info = models.AutoField(primary_key=True)
    tb_task_info_name = models.CharField(max_length=45)
    tb_task_info_type = models.CharField(max_length=45)
    tb_task_info_content = models.CharField(max_length=500)
    tb_task_info_user_id = models.CharField(max_length=45)
    tb_task_info_createtime = models.CharField(max_length=100)
    tb_task_info_status = models.CharField(max_length=45)
    tb_task_info_delflag = models.IntegerField()
    tb_task_info_canceltime = models.CharField(max_length=100)
    tb_task_info_starttime = models.CharField(max_length=100)
    tb_task_info_endtime = models.CharField(max_length=100)
    tb_task_info_expire_date = models.CharField(max_length=100)
    objects = TbTaskInfoManager()
    class Meta:
        managed = False
        db_table = 'tb_task_info'