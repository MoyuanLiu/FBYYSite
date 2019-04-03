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

class KckQueryForm(forms.Form):
    kckproductid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '宝贝ID', 'class': 'form-control'}))
    kckproductcolornum = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '货号(到色)', 'class': 'form-control'}))
    kckproductcategory = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': '类目', 'class': 'form-control'}))
    kckshelfdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    kckshelfdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '上架日期:yyyy-mm-dd'}))
    kckseldepart = forms.CharField(required=False)
    kckselstore = forms.CharField(required=False)

class KckAddForm(forms.Form):
    kckproductid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '宝贝ID', 'class': 'form-control'}))
    kckproductcolornum = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '货号(到色)', 'class': 'form-control'}))
    kckproductcategory = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': '类目', 'class': 'form-control'}))
    kckshelfdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '上架日期:yyyy-mm-dd'}))
    kckseldepart = forms.CharField(required=False)
    kckselstore = forms.CharField(required=False)

class KckEditForm(forms.Form):
    kckid = forms.CharField(required=False)
    kckproductid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '宝贝ID', 'class': 'form-control'}))
    kckproductcolornum = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': '货号(到色)', 'class': 'form-control'}))
    kckproductcategory = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '类目', 'class': 'form-control'}))
    kckshelfdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '上架日期:yyyy-mm-dd'}))
    kckseldepart = forms.CharField(required=False)
    kckselstore = forms.CharField(required=False)