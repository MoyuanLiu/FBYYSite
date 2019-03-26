from django.db import models

# Create your models here.
class TbRoleManager(models.Manager):
    def create_new_role(self,formdata,createtime):
        self.create(tb_role_code=formdata['rolecode'], tb_role_name=formdata['rolename'], tb_role_module_list=formdata['selrolemodulelist'],tb_role_function_list=formdata['selrolefunctionlist'],
                     tb_role_createtime=createtime,tb_role_default_flag=0)
    def get_role_by_id(self,roleid):
        return self.get(idtb_role = roleid)

    def get_roleinfo_list(self,rolelist):
        roleinfolist=list()
        for role in rolelist:
            roleinfo = {}
            roleinfo['idtb_role'] = role.idtb_role
            roleinfo['tb_role_code'] = role.tb_role_code
            roleinfo['tb_role_name'] = role.tb_role_name
            roleinfo['tb_role_module_list'] = role.tb_role_module_list
            roleinfo['tb_role_module_name_list'] = TbModule.objects.get_module_name_list_by_code_list(role.tb_role_module_list)
            roleinfo['tb_role_function_name_list'] = TbFunction.objects.get_function_name_list_by_code_list(role.tb_role_function_list)
            roleinfo['tb_role_default_flag'] = role.tb_role_default_flag
            if role.tb_role_default_flag:
                roleinfo['tb_role_default_flag'] = "默认角色"
            else:
                roleinfo['tb_role_default_flag'] = "非默认"
            roleinfo['tb_role_createtime'] = role.tb_role_createtime
            roleinfolist.append(roleinfo)
        return roleinfolist

    def get_role_name_by_role_id(self,roleid):
        return self.get(idtb_role = roleid).tb_role_name

class TbRole(models.Model):
    idtb_role = models.AutoField(primary_key=True)
    tb_role_code = models.CharField(max_length=45)
    tb_role_name = models.CharField(max_length=45)
    tb_role_module_list = models.CharField(max_length=500)
    tb_role_function_list = models.CharField(max_length=500)
    tb_role_createtime = models.CharField(max_length=100)
    tb_role_default_flag = models.IntegerField()

    objects = TbRoleManager()

    class Meta:
        managed = False
        db_table = 'tb_role'


class TbModuleManager(models.Manager):
    def get_all_modules(self):
        return list(self.all())

    def get_module_name_by_code(self,modulecode):
        return self.get(tb_module_code = modulecode).tb_module_name

    def get_module_name_list_by_code_list(self,modulecodeliststr):
        modulnamelist = []
        if modulecodeliststr=='':
            modulecodelist = []
        else:
            modulecodelist = eval(modulecodeliststr)
        for modulecode in modulecodelist:
            modulnamelist.append(TbModule.objects.get_module_name_by_code(modulecode))
        return modulnamelist

class TbModule(models.Model):
    idtb_module = models.AutoField(primary_key=True)
    tb_module_code = models.CharField(max_length=45)
    tb_module_name = models.CharField(max_length=45)
    objects = TbModuleManager()
    class Meta:
        managed = False
        db_table = 'tb_module'

class TbFunctionManager(models.Manager):
    def get_all_functions_by_module(self,modulecode):
        return self.filter(tb_function_module_code=modulecode)

    def ger_all_functions(self):
        return list(self.all())

    def get_function_name_by_code(self,functioncode):
        return self.get(tb_function_code = functioncode).tb_function_name

    def get_function_name_list_by_code_list(self,functioncodeliststr):
        functionnamelist = []
        if functioncodeliststr=='':
            functioncodelist = []
        else:
            functioncodelist = eval(functioncodeliststr)
        for functioncode in functioncodelist:
            functionnamelist.append(TbFunction.objects.get_function_name_by_code(functioncode))
        return functionnamelist

class TbFunction(models.Model):
    idtb_function = models.AutoField(primary_key=True)
    tb_function_code = models.CharField(max_length=45)
    tb_function_name = models.CharField(max_length=45)
    tb_function_href = models.CharField(max_length=200)
    tb_function_module_code = models.CharField(max_length=45)
    objects = TbFunctionManager()
    class Meta:
        managed = False
        db_table = 'tb_function'

class TbUserRoleManager(models.Manager):
    def get_user_role_by_user_id(self,userid):
        return self.get(tb_user_role_userid=userid)

class TbUserRole(models.Model):
    idtb_user_role = models.AutoField(primary_key=True)
    tb_user_role_userid = models.IntegerField()
    tb_user_role_roleid = models.IntegerField()
    objects = TbUserRoleManager()
    class Meta:
        managed = False
        db_table = 'tb_user_role'


class TbPermissionTypeManager(models.Manager):
    def get_permission_type_name(self,typecode):
        return self.get(tb_permission_type_code = typecode).tb_permission_type_name

class TbPermissionType(models.Model):
    idtb_permission_type = models.AutoField(primary_key=True)
    tb_permission_type_code = models.CharField(max_length=45)
    tb_permission_type_name = models.CharField(max_length=45)
    objects = TbPermissionTypeManager()
    class Meta:
        managed = False
        db_table = 'tb_permission_type'

class TbUserRolePermissionManage(models.Model):
    idtb_user_role_permission_manage = models.AutoField(primary_key=True)
    tb_user_role_permission_manage_user_id = models.CharField(max_length=45)
    tb_user_role_permission_manage_function_code = models.CharField(max_length=45)
    tb_user_role_permission_manage_permission_type_code = models.CharField(max_length=45)
    tb_user_role_permission_manage_permission_range = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tb_user_role_permission_manage'
