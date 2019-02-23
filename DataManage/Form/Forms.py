from django import forms

class ProductQueryForm(forms.Form):
    productid = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品ID','class': 'form-control'}))
    productname = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品名称','class': 'form-control'}))
    productnum = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品货号','class': 'form-control'}))
    seldepart = forms.CharField(required=False)
    selstore = forms.CharField(required=False)
    productcaldatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    productimportdatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    productcaldate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'商品统计日期:年/月/日'}))
    productimportdate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'数据导入日期:年/月/日'}))

class ProductUploadForm(forms.Form):
    seldepart = forms.CharField(required=False)
    selstore = forms.CharField(required=False)
    uploadfilename = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    uploadFile = forms.FileField(required=True,widget=forms.FileInput(attrs={'class': 'custom-file-input',"accept":".xlsx"}))

class ProductUploadTaskQueryForm(forms.Form):
    taskid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入任务ID', 'class': 'form-control'}))
    taskuploadfilename = forms.CharField(required=False, max_length=50,widget=forms.TextInput(attrs={'placeholder': '请输入上传文件名称', 'class': 'form-control'}))
    taskcreatedatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskexpiredateewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskcanceldatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskstartdateewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskenddateewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    seltaskstatus = forms.CharField(required=False)
    taskcreatedate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务创建日期:年/月/日'}))
    taskexpiredate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务过期日期:年/月/日'}))
    taskcanceldate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务取消日期:年/月/日'}))
    taskstartdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务开始日期:年/月/日'}))
    taskenddate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务结束日期:年/月/日'}))



