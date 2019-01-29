from django.db import models
import datetime

# Create your models here.
class TbUserInfoManager(models.Manager):
    def get_user_by_account(self,account):
        return self.get(tb_user_info_email=account)
    def create_new_user(self,name,nickname,email,pwd,departcode,storecode,isactive,issuperuser,datejoined):
        self.create(tb_user_info_name = name,tb_user_info_nickname = nickname,tb_user_info_email = email,tb_user_info_pwd = pwd,tb_user_info_department_code = departcode,
                    tb_user_info_store_code = storecode,tb_user_info_isactive = isactive,tb_user_info_issuperuser = issuperuser,tb_user_info_datejoined = datejoined)

class TbUserInfo(models.Model):
    idtb_user_info = models.AutoField(primary_key=True)
    tb_user_info_name = models.CharField(max_length=45, blank=True, null=True)
    tb_user_info_nickname = models.CharField(max_length=45, blank=True, null=True)
    tb_user_info_email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    tb_user_info_pwd = models.CharField(unique=True, max_length=100, blank=True, null=True)
    tb_user_info_department_code = models.CharField(max_length=45, blank=True, null=True)
    tb_user_info_store_code = models.CharField(max_length=45, blank=True, null=True)
    tb_user_info_isactive = models.IntegerField()
    tb_user_info_issuperuser = models.IntegerField()
    tb_user_info_last_login = models.CharField(max_length=45, blank=True, null=True)
    tb_user_info_datejoined = models.CharField(max_length=45, blank=True, null=True)
    objects = TbUserInfoManager()

    def __Unicode__(self):
        return self.tb_user_info_name
    class Meta:
        managed = False
        db_table = 'tb_user_info'

class TbDepartmentInfoManager(models.Manager):
    def get_all_departments(self):
        return list(self.all())

class TbDepartmentInfo(models.Model):
    idtb_department_info = models.AutoField(primary_key=True)
    tb_department_info_code = models.CharField(unique=True, max_length=45, blank=True, null=True)
    tb_department_info_name = models.CharField(unique=True, max_length=45, blank=True, null=True)
    objects = TbDepartmentInfoManager()
    class Meta:
        managed = False
        db_table = 'tb_department_info'

class TbStoreInfoManager(models.Manager):
    def get_all_stores_by_dapart(self,dapartmentcode):
        return self.filter(tb_store_info_department_code=dapartmentcode)

class TbStoreInfo(models.Model):
    idtb_store = models.AutoField(primary_key=True)
    tb_store_code = models.CharField(max_length=45)
    tb_store_name = models.CharField(max_length=45)
    tb_store_info_department_code = models.CharField(max_length=45)
    objects = TbStoreInfoManager()
    class Meta:
        managed = False
        db_table = 'tb_store_info'