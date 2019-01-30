from django.db import models
import datetime

# Create your models here.
class TbUserInfoManager(models.Manager):
    def get_user_by_account(self,account):
        return self.get(tb_user_info_email=account)
    def create_new_user(self,name,nickname,email,pwd,departcode,storecode,isactive,issuperuser,datejoined):
        self.create(tb_user_info_name = name,tb_user_info_nickname = nickname,tb_user_info_email = email,tb_user_info_pwd = pwd,tb_user_info_department_code = departcode,
                    tb_user_info_store_code = storecode,tb_user_info_isactive = isactive,tb_user_info_issuperuser = issuperuser,tb_user_info_datejoined = datejoined)
    def get_userinfo_list(self):
        userlist = self.all()
        userinfolist=[]
        for user in userlist:
            userinfo = {}
            userinfo['tb_user_info_name'] = user.tb_user_info_name
            userinfo['tb_user_info_nickname'] = user.tb_user_info_nickname
            userinfo['tb_user_info_email'] = user.tb_user_info_email
            userinfo['tb_user_info_pwd'] = user.tb_user_info_pwd
            userinfo['tb_user_info_department_code'] = user.tb_user_info_department_code
            userinfo['tb_user_info_department_name'] = TbDepartmentInfo.objects.get_departmentname_by_code(user.tb_user_info_department_code)
            userinfo['tb_user_info_store_code'] = user.tb_user_info_store_code
            if user.tb_user_info_store_code=='Other':
                userinfo['tb_user_info_store_name'] = "非店铺"
            else:
                userinfo['tb_user_info_store_name'] = TbStoreInfo.objects.get_storename_by_storecode_by_dapartcode(user.tb_user_info_store_code,user.tb_user_info_department_code)
            userinfo['tb_user_info_isactive'] = user.tb_user_info_isactive
            if user.tb_user_info_isactive:
                userinfo['tb_user_info_status'] = "已激活"
            else:
                userinfo['tb_user_info_status'] = "未激活"
            userinfo['tb_user_info_issuperuser'] = user.tb_user_info_issuperuser
            if user.tb_user_info_issuperuser:
                userinfo['tb_user_info_superuser'] = "超级管理员"
            else:
                userinfo['tb_user_info_superuser'] = "非超级管理员"
            userinfo['tb_user_info_last_login'] = user.tb_user_info_last_login
            userinfo['tb_user_info_datejoined'] = user.tb_user_info_datejoined
            userinfolist.append(userinfo)
        return userinfolist

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
    def get_departmentname_by_code(self,code):
        depart = self.get(tb_department_info_code = code)
        return depart.tb_department_info_name

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
    def get_storename_by_storecode_by_dapartcode(self,storecode,dapartcode):
        return self.get(tb_store_code = storecode,tb_store_info_department_code = dapartcode)

class TbStoreInfo(models.Model):
    idtb_store = models.AutoField(primary_key=True)
    tb_store_code = models.CharField(max_length=45)
    tb_store_name = models.CharField(max_length=45)
    tb_store_info_department_code = models.CharField(max_length=45)
    objects = TbStoreInfoManager()
    class Meta:
        managed = False
        db_table = 'tb_store_info'