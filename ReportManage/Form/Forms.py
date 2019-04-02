from django import forms

class CtsQueryForm(forms.Form):
    ctsproductnum = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品编码','class': 'form-control'}))
    ctssellcountmin = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品销量下限','class': 'form-control'}))
    ctssellcountmax = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入商品销量上限', 'class': 'form-control'}))
    ctscaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    ctscaldate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'统计日期:yyyy-mm-dd'}))
    ctscaldepart = forms.CharField(required=False)

class CtsMakeForm(forms.Form):
    ctsmakedate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'制作日期:yyyy-mm-dd'}))
    ctsmakedepart = forms.CharField(required=False)