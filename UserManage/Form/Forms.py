from django import forms
from Utils.DateTimeUtil import is_valid_date
import time


class UserEditForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入真实姓名','class': 'form-control'}))
    usernickname = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入公司内部花名','class': 'form-control'}))
    pwd = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'请输入密码','class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱地址', 'class': 'form-control'}))
    seldepart = forms.CharField(required=True)
    selstore = forms.CharField(required=True)
    userid = forms.CharField(required=True,widget=forms.HiddenInput())
    superuserwhether = forms.CharField(required=True)
    activeaccountwhether = forms.CharField(required=True)


class UserAddForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入真实姓名','class': 'form-control'}))
    usernickname = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入公司内部花名','class': 'form-control'}))
    pwd = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'请输入密码','class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱地址', 'class': 'form-control'}))
    seldepart = forms.CharField(required=True)
    selstore = forms.CharField(required=True)
    superuserwhether = forms.CharField(required=True)


class UserQueryForm(forms.Form):
    queryusername = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'用户名','class': 'form-control'}))
    queryusernickname = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'用户花名','class': 'form-control'}))
    queryemail = forms.EmailField(required=False,widget=forms.EmailInput(attrs={'placeholder': '用户邮箱', 'class': 'form-control'}))
    queryuserdepart = forms.CharField(required=False)
    queryuserstore = forms.CharField(required=False)
    querysuperuserwhether = forms.CharField(required=True)
    queryactiveaccountwhether = forms.CharField(required=True)
    querycreatedateflag = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    querysuperuserwhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    queryactiveaccountwhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    querycreatedate=forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'用户创建日期:年/月/日'}))

    def clean_querycreatedate(self):
        querycreatedateinput = self.cleaned_data['querycreatedate']
        if self.cleaned_data['querycreatedateflag']:
            pattern = "%Y/%m/%d"
            if not is_valid_date(querycreatedateinput,pattern):
                raise forms.ValidationError("日期格式不对！！")
        return querycreatedateinput


class AccountEditForm(forms.Form):
    username = forms.CharField(required=True, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入真实姓名', 'class': 'form-control'}))
    usernickname = forms.CharField(required=True, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入公司内部花名', 'class': 'form-control'}))
    seldepart = forms.CharField(required=True)
    selstore = forms.CharField(required=True)
    userid = forms.CharField(required=True, widget=forms.HiddenInput())


class PwdChangeForm(forms.Form):
    email = forms.CharField(required=True,widget=forms.HiddenInput())
    pwd = forms.CharField(required=True, min_length=6,widget=forms.PasswordInput(attrs={'placeholder': '请输入密码', 'class': 'form-control'}))
    confirmpwd = forms.CharField(required=True, min_length=6,widget=forms.PasswordInput(attrs={'placeholder': '请再次输入密码', 'class': 'form-control'}))

    def clean_confirmpwd(self):
        pwd = self.cleaned_data['pwd']
        confirmpwd = self.cleaned_data['confirmpwd']
        if confirmpwd != pwd:
            raise forms.ValidationError("两次密码输入不一致！！")


