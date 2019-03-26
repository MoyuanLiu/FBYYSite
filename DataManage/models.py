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
    def newtask(self,taskname,tasktype,taskcontent,taskuserid,taskcreatetime,taskstatus,taskexpiredate,taskinfocode):
        self.create(tb_task_info_name=taskname,tb_task_info_type=tasktype,tb_task_info_content=taskcontent,tb_task_info_user_id=taskuserid,tb_task_info_createtime=taskcreatetime,tb_task_info_status=taskstatus,tb_task_info_expire_date=taskexpiredate,tb_task_info_delflag=0,tb_task_info_code=taskinfocode)

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
    tb_task_info_code = models.CharField(max_length=45)
    objects = TbTaskInfoManager()
    class Meta:
        managed = False
        db_table = 'tb_task_info'

class TbOrder(models.Model):
    idtb_order = models.AutoField(primary_key=True)
    tb_order_store_name = models.CharField(max_length=45)
    tb_order_id = models.CharField(max_length=45)
    tb_order_sys_id = models.CharField(max_length=45)
    tb_order_mark = models.CharField(max_length=45, blank=True, null=True)
    tb_order_actual_pay_count = models.FloatField(blank=True, null=True)
    tb_order_benifit_count = models.FloatField(blank=True, null=True)
    tb_order_storage_code = models.CharField(max_length=45)
    tb_order_storage_name = models.CharField(max_length=45)
    tb_order_buyyer_review = models.CharField(max_length=500, blank=True, null=True)
    tb_order_comment = models.CharField(max_length=1000, blank=True, null=True)
    tb_order_print_comment = models.CharField(max_length=45, blank=True, null=True)
    tb_order_sys_order_status = models.CharField(max_length=45)
    tb_order_online_order_status = models.CharField(max_length=45)
    tb_order_patch_num = models.CharField(max_length=45, blank=True, null=True)
    tb_order_detail_status = models.CharField(max_length=45)
    tb_order_old_order_id = models.CharField(max_length=45)
    tb_order_product_code = models.CharField(max_length=45)
    tb_order_product_name = models.CharField(max_length=300)
    tb_order_spec_name = models.CharField(max_length=45)
    tb_order_online_product_code = models.CharField(max_length=45)
    tb_order_online_product_title = models.CharField(max_length=45)
    tb_order_online_spec = models.CharField(max_length=45)
    tb_order_price = models.FloatField()
    tb_order_benifit_price = models.FloatField()
    tb_order_num = models.IntegerField()
    tb_order_unit = models.CharField(max_length=45, blank=True, null=True)
    tb_order_suppose_money = models.FloatField()
    tb_order_sale_money = models.FloatField()
    tb_order_detail_comment = models.CharField(max_length=45, blank=True, null=True)
    tb_order_invoice_title = models.CharField(max_length=45, blank=True, null=True)
    tb_order_invoice_content = models.CharField(max_length=45, blank=True, null=True)
    tb_order_invoice_bank = models.CharField(max_length=45)
    tb_order_invoice_bank_account = models.CharField(max_length=45, blank=True, null=True)
    tb_order_invoice_tax_number = models.CharField(max_length=45, blank=True, null=True)
    tb_order_invoice_address = models.CharField(max_length=45, blank=True, null=True)
    tb_order_invoice_tel = models.CharField(max_length=45, blank=True, null=True)
    tb_order_invoice_email = models.CharField(max_length=45, blank=True, null=True)
    tb_order_express_company = models.CharField(max_length=45)
    tb_order_express_num = models.CharField(max_length=45, blank=True, null=True)
    tb_order_express_cost = models.FloatField(blank=True, null=True)
    tb_order_weight = models.FloatField(blank=True, null=True)
    tb_order_volume = models.FloatField(blank=True, null=True)
    tb_order_post_cost = models.FloatField(blank=True, null=True)
    tb_order_service_cost = models.FloatField(blank=True, null=True)
    tb_order_account = models.CharField(max_length=45)
    tb_order_receiver_name = models.CharField(max_length=45)
    tb_order_idcard_num = models.CharField(max_length=45, blank=True, null=True)
    tb_order_receiver_tel = models.CharField(max_length=45)
    tb_order_receiver_province = models.CharField(max_length=45)
    tb_order_receiver_city = models.CharField(max_length=45)
    tb_order_receiver_county = models.CharField(max_length=45)
    tb_order_receiver_detail_address = models.CharField(max_length=500)
    tb_order_post_code = models.CharField(max_length=45)
    tb_order_order_time = models.CharField(max_length=45)
    tb_order_pay_time = models.CharField(max_length=45, blank=True, null=True)
    tb_order_print_time = models.CharField(max_length=45, blank=True, null=True)
    tb_order_send_time = models.CharField(max_length=45, blank=True, null=True)
    tb_order_over_time = models.CharField(max_length=45, blank=True, null=True)
    tb_order_trade_hire_money = models.FloatField(blank=True, null=True)
    tb_order_cdcard_hire_money = models.FloatField(blank=True, null=True)
    tb_order_return_score = models.FloatField(blank=True, null=True)
    tb_order_checker = models.CharField(max_length=45, blank=True, null=True)
    tb_order_printer = models.CharField(max_length=45, blank=True, null=True)
    tb_order_distributor = models.CharField(max_length=45, blank=True, null=True)
    tb_order_surveyor = models.CharField(max_length=45, blank=True, null=True)
    tb_order_packer = models.CharField(max_length=45, blank=True, null=True)
    tb_order_weighter = models.CharField(max_length=45, blank=True, null=True)
    tb_order_sender = models.CharField(max_length=45, blank=True, null=True)
    tb_order_salesman = models.CharField(max_length=45, blank=True, null=True)
    tb_order_click_farm_flag = models.IntegerField(blank=True, null=True)
    tb_order_order_date = models.CharField(max_length=45)
    tb_order_store_code = models.CharField(max_length=45)
    tb_order_depart_code = models.CharField(max_length=45)
    tb_order_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_order'

class TbStorage(models.Model):
    idtb_storage = models.AutoField(primary_key=True)
    tb_storage_product_code = models.CharField(max_length=45)
    tb_storage_product_id = models.CharField(max_length=45)
    tb_storage_product_name = models.CharField(max_length=100)
    tb_storage_spec_name = models.CharField(max_length=100)
    tb_storage_product_num = models.CharField(max_length=45)
    tb_storage_catalogue = models.CharField(max_length=45)
    tb_storage_actual_stock = models.IntegerField()
    tb_storage_lock_stock = models.IntegerField()
    tb_storage_available_stock = models.IntegerField()
    tb_storage_intransit_stock = models.IntegerField()
    tb_storage_import_date = models.CharField(max_length=45)
    tb_storage_depart_code = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_storage'

class TbZtc(models.Model):
    idtb_ztc = models.AutoField(primary_key=True)
    tb_ztc_caldate = models.CharField(max_length=45)
    tb_ztc_plan_name = models.CharField(max_length=45)
    tb_ztc_product_name = models.CharField(max_length=100)
    tb_ztc_search_type = models.CharField(max_length=45)
    tb_ztc_traffic_source = models.CharField(max_length=45)
    tb_ztc_impression_count = models.IntegerField(blank=True, null=True)
    tb_ztc_click_count = models.IntegerField(blank=True, null=True)
    tb_ztc_cost = models.IntegerField(blank=True, null=True)
    tb_ztc_click_percent = models.FloatField(blank=True, null=True)
    tb_ztc_avg_click_cost = models.FloatField(blank=True, null=True)
    tb_ztc_thousand_impression_cost = models.FloatField(blank=True, null=True)
    tb_ztc_click_turn_percent = models.FloatField(blank=True, null=True)
    tb_ztc_direct_deal_money = models.IntegerField(blank=True, null=True)
    tb_ztc_direct_deal_count = models.IntegerField(blank=True, null=True)
    tb_ztc_undirect_deal_money = models.IntegerField(blank=True, null=True)
    tb_ztc_undirect_deal_count = models.IntegerField(blank=True, null=True)
    tb_ztc_deal_money = models.IntegerField(blank=True, null=True)
    tb_ztc_deal_count = models.IntegerField(blank=True, null=True)
    tb_ztc_product_collect_count = models.IntegerField(blank=True, null=True)
    tb_ztc_store_collect_count = models.IntegerField(blank=True, null=True)
    tb_ztc_total_collect_count = models.IntegerField(blank=True, null=True)
    tb_ztc_io_ratio = models.FloatField(blank=True, null=True)
    tb_ztc_direct_cart_count = models.IntegerField(blank=True, null=True)
    tb_ztc_undirect_cart_count = models.IntegerField(blank=True, null=True)
    tb_ztc_total_cart_count = models.IntegerField(blank=True, null=True)
    tb_ztc_store_code = models.CharField(max_length=45)
    tb_ztc_depart_code = models.CharField(max_length=45)
    tb_ztc_import_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tb_ztc'

class TbStoreCost(models.Model):
    idtb_store_cost = models.AutoField(primary_key=True)
    tb_store_cost_cal_date = models.CharField(max_length=45)
    tb_store_cost_ztc = models.FloatField()
    tb_store_cost_zszw = models.FloatField()
    tb_store_cost_tbk = models.FloatField()
    tb_store_cost_store_code = models.CharField(max_length=45)
    tb_store_cost_depart_code = models.CharField(max_length=45)
    tb_store_cost_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_cost'

class TbStoreFlow(models.Model):
    idtb_store_flow = models.AutoField(primary_key=True)
    tb_store_flow_caldate = models.CharField(db_column='tb_store_flow_calDate', max_length=45)  # Field name made lowercase.
    tb_store_flow_visitors = models.IntegerField()
    tb_store_flow_views = models.IntegerField()
    tb_store_flow_product_visitors = models.IntegerField()
    tb_store_flow_product_views = models.IntegerField()
    tb_store_flow_avg_stoptime = models.FloatField()
    tb_store_flow_jump_percent = models.FloatField()
    tb_store_flow_views_avg = models.FloatField()
    tb_store_flow_visitors_old = models.IntegerField()
    tb_store_flow_visitors_new = models.IntegerField()
    tb_store_flow_source = models.CharField(max_length=45)
    tb_store_flow_store_code = models.CharField(max_length=45)
    tb_store_flow_depart_code = models.CharField(max_length=45)
    tb_store_flow_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_flow'

class TbStoreInteraction(models.Model):
    idtb_store_interaction = models.AutoField(db_column='idtb_store_Interaction', primary_key=True)  # Field name made lowercase.
    tb_store_interaction_cal_date = models.CharField(db_column='tb_store_Interaction_cal_date', max_length=45)  # Field name made lowercase.
    tb_store_interaction_product_collect_buyyers = models.IntegerField(db_column='tb_store_Interaction_product_collect_buyyers')  # Field name made lowercase.
    tb_store_interaction_product_collects = models.IntegerField(db_column='tb_store_Interaction_product_collects')  # Field name made lowercase.
    tb_store_interaction_product_adds = models.IntegerField(db_column='tb_store_Interaction_product_adds')  # Field name made lowercase.
    tb_store_interaction_product_add_items = models.IntegerField(db_column='tb_store_Interaction_product_add_items')  # Field name made lowercase.
    tb_store_interaction_store_source = models.CharField(max_length=45)
    tb_store_interaction_store_code = models.CharField(db_column='tb_store_Interaction_store_code', max_length=45)  # Field name made lowercase.
    tb_store_interaction_depart_code = models.CharField(max_length=45)
    tb_store_interaction_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_interaction'

class TbStoreLogistic(models.Model):
    idtb_store_logistic = models.AutoField(primary_key=True)
    tb_store_logistic_cal_date = models.CharField(max_length=45)
    tb_store_logistic_pay_parent_orders = models.IntegerField()
    tb_store_logistic_pay_child_orders = models.IntegerField()
    tb_store_logistic_receive_packages = models.IntegerField()
    tb_store_logistic_send_packages = models.IntegerField()
    tb_store_logistic_dispatch_packages = models.IntegerField()
    tb_store_logistic_signed_packages = models.IntegerField()
    tb_store_logistic_avg_pay_sign_time = models.FloatField()
    tb_store_logistic_store_code = models.CharField(max_length=45)
    tb_store_logistic_depart_code = models.CharField(max_length=45)
    tb_store_logistic_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_logistic'

class TbStoreReview(models.Model):
    idtb_store_review = models.AutoField(primary_key=True)
    tb_store_review_cal_date = models.CharField(max_length=45)
    tb_store_review_reviews = models.IntegerField()
    tb_store_review_picture_reviews = models.IntegerField()
    tb_store_review_positive_reviews = models.IntegerField()
    tb_store_review_critical_reviews = models.IntegerField()
    tb_store_review_positive_reviews_old = models.IntegerField()
    tb_store_review_critical_reviews_old = models.IntegerField()
    tb_store_review_description_score = models.FloatField()
    tb_store_review_logistics_score = models.FloatField()
    tb_store_review_attitude_score = models.FloatField()
    tb_store_review_store_code = models.CharField(max_length=45)
    tb_store_review_depart_code = models.CharField(max_length=45)
    tb_store_review_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_review'

class TbStoreService(models.Model):
    idtb_store_service = models.AutoField(primary_key=True)
    tb_store_service_cal_date = models.CharField(max_length=45)
    tb_store_service_success_return_money = models.FloatField()
    tb_store_service_pay_buyyers_old_money = models.FloatField(blank=True, null=True)
    tb_store_service_store_code = models.CharField(max_length=45)
    tb_store_service_depart_code = models.CharField(max_length=45)
    tb_store_service_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_service'

class TbStoreTrade(models.Model):
    idtb_store_trade = models.AutoField(primary_key=True)
    tb_store_trade_caldate = models.CharField(max_length=45)
    tb_store_trade_pay_money = models.FloatField()
    tb_store_trade_pay_buyyers = models.IntegerField()
    tb_store_trade_pay_childorders = models.IntegerField()
    tb_store_trade_pay_items = models.IntegerField()
    tb_store_trade_order_money = models.IntegerField()
    tb_store_trade_order_buyyers = models.IntegerField()
    tb_store_trade_order_items = models.IntegerField()
    tb_store_trade_buyyers_avg_money = models.FloatField()
    tb_store_trade_uv = models.FloatField()
    tb_store_trade_pay_buyyers_old = models.IntegerField()
    tb_store_trade_pay_products = models.IntegerField()
    tb_store_trade_store_source = models.CharField(max_length=45)
    tb_store_trade_store_code = models.CharField(max_length=45)
    tb_store_trade_depart_code = models.CharField(max_length=45)
    tb_store_trade_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_trade'

class TbStoreTurn(models.Model):
    idtb_store_turn = models.AutoField(primary_key=True)
    tb_store_turn_caldate = models.CharField(max_length=45)
    tb_store_turn_order_turn_percent = models.FloatField()
    tb_store_turn_pay_turn_percent = models.FloatField()
    tb_store_turn_order_pay_turn_percent = models.FloatField()
    tb_store_turn_collect_buyyers = models.IntegerField()
    tb_store_turn_store_source = models.CharField(max_length=45)
    tb_store_turn_store_code = models.CharField(max_length=45)
    tb_store_turn_depart_code = models.CharField(max_length=45)
    tb_store_turn_import_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_store_turn'
