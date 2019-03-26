from django import forms

class ProductQueryForm(forms.Form):
    productid = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品ID','class': 'form-control'}))
    productname = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品名称','class': 'form-control'}))
    productnum = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入商品货号','class': 'form-control'}))
    queryproductdepart = forms.CharField(required=False)
    queryproductstore = forms.CharField(required=False)
    productcaldatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    productimportdatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    productcaldate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'商品统计日期:年/月/日'}))
    productimportdate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'数据导入日期:年/月/日'}))

class FileUploadForm(forms.Form):
    uploadfilename = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    uploadFile = forms.FileField(required=True,widget=forms.FileInput(attrs={'class': 'custom-file-input',"accept":".xlsx"}))

class ClickFirmFileUploadForm(forms.Form):
    uploadclickfirmfilename = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    uploadclickfirmFile = forms.FileField(required=True,widget=forms.FileInput(attrs={'class': 'custom-file-input',"accept":".xlsx"}))

class UploadTaskQueryForm(forms.Form):
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

class ZTCQueryForm(forms.Form):
    ztcplanname = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入推广计划名称', 'class': 'form-control'}))
    ztcproductname = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder':'请输入宝贝名称','class': 'form-control'}))
    ztcsearchtypeflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    ztctrafficsouceflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    ztcsearchtype = forms.CharField(required=False)
    ztctrafficsouce = forms.CharField(required=False)
    queryztcdepart = forms.CharField(required=False)
    queryztcstore = forms.CharField(required=False)
    ztccaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    ztcimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    ztccaldate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '直通车统计日期:年/月/日'}))
    ztcimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))

class OrderQueryForm(forms.Form):
    orderid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入订单ID', 'class': 'form-control'}))
    ordersysid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入系统单号', 'class': 'form-control'}))
    onlineproductcode = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入线上商品编码', 'class': 'form-control'}))
    orderdetailstatus = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入明细状态', 'class': 'form-control'}))
    queryorderdepart = forms.CharField(required=False)
    queryorderstore = forms.CharField(required=False)
    orderclickfirmflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    orderclickfirm = forms.CharField(required=False)

    queryorderdatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    queryorderdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '下单日期:年/月/日'}))
    querypaydatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    querypaydate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '付款日期:年/月/日'}))
    queryprintdatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    queryprintdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '打单日期:年/月/日'}))
    querysenddatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    querysenddate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '发货日期:年/月/日'}))
    queryoverdatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    queryoverdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '完成日期:年/月/日'}))
    queryimportdatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    queryimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '导入日期:年/月/日'}))

class StorageQueryForm(forms.Form):
    storageproductid = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入商品编码', 'class': 'form-control'}))
    storagespecname = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入规格名称', 'class': 'form-control'}))
    storageproductnum = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入货号', 'class': 'form-control'}))
    storagecatalogue = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'placeholder': '请输入分类', 'class': 'form-control'}))
    queryimportdatewhetherflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    querystoragedepart = forms.CharField(required=False)
    queryimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '导入日期:年/月/日'}))

class StoreCostQueryForm(forms.Form):
    querystorecostdepart = forms.CharField(required=False)
    querystorecoststore = forms.CharField(required=False)
    storecostcaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storecostimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storecostcaldate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storecostimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))

class StoreFlowQueryForm(forms.Form):
    querystoreflowdepart = forms.CharField(required=False)
    querystoreflowstore = forms.CharField(required=False)
    storeflowcaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeflowimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeflowcaldate = forms.DateField(required=False, widget=forms.DateInput( attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storeflowimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))
    storeflowstoresourceflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeflowstoresource = forms.CharField(required=False)


class StoreLogisticQueryForm(forms.Form):
    querystorelogisticdepart = forms.CharField(required=False)
    querystorelogisticstore = forms.CharField(required=False)
    storelogisticcaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storelogisticimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storelogisticcaldate = forms.DateField(required=False, widget=forms.DateInput( attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storelogisticimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))

class StoreReviewQueryForm(forms.Form):
    querystorereviewdepart = forms.CharField(required=False)
    querystorereviewstore = forms.CharField(required=False)
    storereviewcaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storereviewimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storereviewcaldate = forms.DateField(required=False, widget=forms.DateInput( attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storereviewimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))

class StoreServiceQueryForm(forms.Form):
    querystoreservicedepart = forms.CharField(required=False)
    querystoreservicestore = forms.CharField(required=False)
    storeservicecaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeserviceimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeservicecaldate = forms.DateField(required=False, widget=forms.DateInput( attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storeserviceimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))

class StoreTradeQueryForm(forms.Form):
    querystoretradedepart = forms.CharField(required=False)
    querystoretradestore = forms.CharField(required=False)
    storetradecaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storetradeimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storetradecaldate = forms.DateField(required=False, widget=forms.DateInput( attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storetradeimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))
    storetradestoresourceflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storetradestoresource = forms.CharField(required=False)

class StoreTurnQueryForm(forms.Form):
    querystoreturndepart = forms.CharField(required=False)
    querystoreturnstore = forms.CharField(required=False)
    storeturncaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeturnimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeturncaldate = forms.DateField(required=False, widget=forms.DateInput( attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storeturnimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))
    storeturnstoresourceflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeturnstoresource = forms.CharField(required=False)

class StoreInteractionQueryForm(forms.Form):
    querystoreinteractiondepart = forms.CharField(required=False)
    querystoreinteractionstore = forms.CharField(required=False)
    storeinteractioncaldateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeinteractionimportdateflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeinteractioncaldate = forms.DateField(required=False, widget=forms.DateInput( attrs={'class': 'form-control', 'placeholder': '统计日期:年/月/日'}))
    storeinteractionimportdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '数据导入日期:年/月/日'}))
    storeinteractionstoresourceflag = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    storeinteractionstoresource = forms.CharField(required=False)










