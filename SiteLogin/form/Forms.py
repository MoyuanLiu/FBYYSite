from django import forms

class RegisteForm(forms.Form):
    username = forms.CharField(required=True,max_length=20)
    usernickname = forms.CharField(required=True,max_length=20)
    pwd = forms.CharField(required=True,min_length=6)
    confirmpwd = forms.CharField(required=True,min_length=6)
    email = forms.EmailField(required=True)
    seldepart = forms.CharField(required=True)
    selstore = forms.CharField(required=True)

    def clean_confirmpwd(self):
        pwd = self.cleaned_data['pwd']
        confirmpwd = self.cleaned_data['confirmpwd']
        if confirmpwd != pwd:
            raise forms.ValidationError("两次密码输入不一致！！")
