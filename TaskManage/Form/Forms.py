from django import forms

class AllTaskQueryForm(forms.Form):
    taskid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入任务ID', 'class': 'form-control'}))
    taskuploadfilename = forms.CharField(required=False, max_length=50,widget=forms.TextInput(attrs={'placeholder': '请输入上传文件名称', 'class': 'form-control'}))
    taskcreatedatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskexpiredateewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskcanceldatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskstartdateewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskenddateewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskuseridflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    taskuserid = forms.CharField(required=False)
    seltaskstatus = forms.CharField(required=False)
    taskcreatedate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务创建日期:年/月/日'}))
    taskexpiredate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务过期日期:年/月/日'}))
    taskcanceldate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务取消日期:年/月/日'}))
    taskstartdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务开始日期:年/月/日'}))
    taskenddate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '任务结束日期:年/月/日'}))