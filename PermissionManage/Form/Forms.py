from django import forms
class RoleQueryForm(forms.Form):
    rolecode = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入角色编码','class': 'form-control'}))
    rolename = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入角色名称','class': 'form-control'}))
    selrolemodule = forms.CharField(required=False)
    selrolefunction = forms.CharField(required=False)
    rolecreatedatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    roledefaultwhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    rolecreatedate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'角色创建日期:年/月/日'}))
    roledefaultwhether = forms.CharField(required=False)

class RoleAddForm(forms.Form):
    rolecode = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入角色编码','class': 'form-control'}))
    rolename = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入角色名称','class': 'form-control'}))
    selrolemodulelist = forms.CharField(required=False,widget=forms.SelectMultiple(attrs={'class': 'form-control','style':'min-width:200px'}))
    selrolefunctionlist = forms.CharField(required=False,widget=forms.SelectMultiple(attrs={'class': 'form-control','style':'min-width:200px'}))

class RoleEditForm(forms.Form):
    rolecode = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入角色编码','class': 'form-control'}))
    rolename = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入角色名称','class': 'form-control'}))
    selrolemodulelist = forms.CharField(required=True,widget=forms.SelectMultiple(attrs={'class': 'form-control','style':'min-width:200px'}))
    selrolefunctionlist = forms.CharField(required=True,widget=forms.SelectMultiple(attrs={'class': 'form-control','style':'min-width:200px'}))
    roleid = forms.CharField(required=True, widget=forms.HiddenInput())

class PermissionQueryForm(forms.Form):
    username = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入真实姓名', 'class': 'form-control'}))
    usernickname = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入公司内部花名', 'class': 'form-control'}))
    seldepart = forms.CharField(required=False)
    selstore = forms.CharField(required=False)
    querysuperuserwhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    querysuperuserwhether = forms.CharField(required=False)
    selrole = forms.CharField(required=False)
    selrolemodule = forms.CharField(required=False)
    selrolefunction = forms.CharField(required=False)
    selpermissiontype = forms.CharField(required=False)

class PermissionEsitForm(forms.Form):
    userid = forms.CharField(required=True, widget=forms.HiddenInput())
    selrole = forms.CharField(required=True)
    selpermission = forms.CharField(required=True,widget=forms.SelectMultiple(attrs={'class': 'form-control','style':'min-width:200px'}))


