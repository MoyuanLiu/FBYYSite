from django import forms

class RegisteForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入真实姓名','class': 'form-control'}))
    usernickname = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入公司内部花名','class': 'form-control'}))
    pwd = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'请输入密码','class': 'form-control'}))
    confirmpwd = forms.CharField(required=True,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':'请再次输入密码','class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'请输入邮箱地址','class': 'form-control'}))
    seldepart = forms.CharField(required=True)
    selstore = forms.CharField(required=True)

    def clean_confirmpwd(self):
        pwd = self.cleaned_data['pwd']
        confirmpwd = self.cleaned_data['confirmpwd']
        if confirmpwd != pwd:
            raise forms.ValidationError("两次密码输入不一致！！")
