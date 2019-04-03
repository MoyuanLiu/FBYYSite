"""FBYYSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path,re_path
from SiteLogin import views as slview
from UserManage import views as umview
from DataManage import views as dmview
from PermissionManage import views as pmview
from TaskManage import views as tmview
from ReportManage import views as rmview

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('fbyysite/login',slview.login),
    path('fbyysite/registe',slview.registe),
    re_path(r'fbyysite/registe/ajaxstores?[^/]+',slview.registe_ajax_store),
    path('fbyysite/index/',slview.requires_login(slview.index)),
    path('fbyysite/about',slview.requires_login(slview.about)),
    re_path(r'fbyysite/active/(.*)',slview.activeaccount),
    re_path(r'fbyysite/jump/(.*)',slview.tmpjump),
    path('fbyysite/index/left',slview.index_left),
    path('fbyysite/index/content',slview.index_content),
    re_path(r'fbyysite/usermanage/pagenum/(\d+)',umview.usermanage),
    path('fbyysite/usermanage/edit/account/usereditcheck',umview.usereditcheck),
    re_path(r'fbyysite/usermanage/edit/account/(.+)',umview.useredit),
    path('fbyysite/usermanage/delete/account/',umview.userdel),
    path('fbyysite/usermanage/add/',umview.useradd),
    re_path(r'fbyysite/usermanage/query/(\d+)',umview.userquery),
    path('fbyysite/logout',slview.logout),
    path('fbyysite/accountmanage',umview.accountmanage),
    path('fbyysite/accountpswchange',umview.accountpwdchange),
    path('fbyysite/accountemailchange',umview.accountemailchange),
    re_path('fbyysite/pwdchange/confirm/(.*)',umview.accountpwdchangeconfirm),
    re_path('fbyysite/emailchange/confirm/(.*)',umview.accountemailchangeconfirm),
    path('fbyysite/pwdchange/change',umview.accountpwdnew),
    re_path(r'fbyysite/datamanage/ztc/pagenum/(\d+)',dmview.ztcmanage),
    re_path(r'fbyysite/datamanage/product/pagenum/(\d+)',dmview.productmanage),
    re_path(r'fbyysite/datamanage/product/query/(\d+)',dmview.productquery),
    path('fbyysite/datamanage/product/upload',dmview.productupload),
    re_path(r'fbyysite/datamanage/product/upload/taskquery/(\d+)',dmview.productuploadtaskquery),
    path('fbyysite/datamanage/upload/taskcancel', dmview.taskcancel),
    re_path(r'fbyysite/rolemanage/pagenum/(\d+)',pmview.rolemanage),
    re_path(r'fbyysite/permission/ajaxfunctions?[^/]+',pmview.permission_ajax_function),
    path('fbyysite/rolemanage/add/',pmview.roleadd),
    re_path(r'fbyysite/rolemanage/edit/(.+)',pmview.roleedit),
    path('fbyysite/rolemanage/roleeditcheck', pmview.roleeditcheck),
    path('fbyysite/rolemanage/default/', pmview.roledefault),
    path('fbyysite/rolemanage/delete/', pmview.roledelete),
    re_path(r'fbyysite/rolemanage/query/(.+)',pmview.rolequery),
    re_path(r'fbyysite/permissionmanage/pagenum/(\d+)',pmview.permissionmanage),
    re_path(r'fbyysite/permissionmanage/edit/(.+)',pmview.assignpermission),
    re_path(r'fbyysite/role/ajaxfunctions?[^/]+',pmview.role_ajax_function),
    path('fbyysite/permissionmanage/permissioneditcheck', pmview.permissioneditcheck),
    re_path(r'fbyysite/permissionmanage/ajaxpermisssiondetail?[^/]+',pmview.user_ajax_permission),
    path('fbyysite/permissionmanage/delete/', pmview.permissiondelete),
    re_path(r'fbyysite/permissionmanage/query/(.+)',pmview.querypermission),
    re_path(r'fbyysite/productmanage/ajaxstores?[^/]+',dmview.product_ajax_store),
    re_path(r'fbyysite/productmanage/uploadajaxstores?[^/]+',dmview.product_upload_ajax_store),
    re_path(r'fbyysite/datamanage/order/pagenum/(\d+)',dmview.ordermanage),
    re_path(r'fbyysite/datamanage/storage/pagenum/(\d+)',dmview.storagemanage),
    path(r'fbyysite/datamanage/store/',dmview.storemanage),
    re_path(r'fbyysite/datamanage/store/storecost/pagenum/(\d+)',dmview.storecostmanage),
    re_path(r'fbyysite/datamanage/store/storeflow/pagenum/(\d+)',dmview.storeflowmanage),
    re_path(r'fbyysite/datamanage/store/storeinteraction/pagenum/(\d+)',dmview.storeinteractionmanage),
    re_path(r'fbyysite/datamanage/store/storelogistic/pagenum/(\d+)',dmview.storelogisticmanage),
    re_path(r'fbyysite/datamanage/store/storereview/pagenum/(\d+)',dmview.storereviewmanage),
    re_path(r'fbyysite/datamanage/store/storeservice/pagenum/(\d+)',dmview.storeservicemanage),
    re_path(r'fbyysite/datamanage/store/storetrade/pagenum/(\d+)',dmview.storetrademanage),
    re_path(r'fbyysite/datamanage/store/storeturn/pagenum/(\d+)',dmview.storeturnmanage),
    re_path(r'fbyysite/ztcmanage/ajaxstores?[^/]+',dmview.ztc_ajax_store),
    re_path(r'fbyysite/datamanage/ztc/query/(\d+)',dmview.ztcquery),
    re_path(r'fbyysite/ztcmanage/uploadajaxstores?[^/]+',dmview.ztc_upload_ajax_store),
    re_path(r'fbyysite/datamanage/order/query/(\d+)',dmview.orderquery),
    re_path(r'fbyysite/ordermanage/ajaxstores?[^/]+',dmview.order_ajax_store),
    re_path(r'fbyysite/ordermanage/uploadajaxstores?[^/]+',dmview.order_upload_ajax_store),
    re_path(r'fbyysite/datamanage/storage/query/(\d+)',dmview.storagequery),
    re_path(r'fbyysite/datamanage/store/storecost/query/(\d+)',dmview.storecostquery),
    re_path(r'fbyysite/datamanage/store/storeflow/query/(\d+)',dmview.storeflowquery),
    re_path(r'fbyysite/datamanage/store/storeinteraction/query/(\d+)',dmview.storeinteractionquery),
    re_path(r'fbyysite/datamanage/store/storelogistic/query/(\d+)',dmview.storelogisticquery),
    re_path(r'fbyysite/datamanage/store/storereview/query/(\d+)',dmview.storereviewquery),
    re_path(r'fbyysite/datamanage/store/storeservice/query/(\d+)',dmview.storeservicequery),
    re_path(r'fbyysite/datamanage/store/storetrade/query/(\d+)',dmview.storetradequery),
    re_path(r'fbyysite/datamanage/store/storeturn/query/(\d+)',dmview.storeturnquery),
    re_path(r'fbyysite/storemanage/ajaxstores?[^/]+',dmview.store_ajax_store),
    re_path(r'fbyysite/storemanage/uploadajaxstores?[^/]+',dmview.store_upload_ajax_store),
    path('fbyysite/datamanage/ztc/upload',dmview.ztcupload),
    path('fbyysite/datamanage/order/upload',dmview.orderupload),
    path('fbyysite/datamanage/order/clickfirm/upload',dmview.orderclickfirmupload),
    path('fbyysite/datamanage/storage/upload',dmview.storageupload),
    path('fbyysite/datamanage/store/upload',dmview.storeupload),
    re_path(r'fbyysite/datamanage/ztc/upload/taskquery/(\d+)',dmview.ztcuploadtaskquery),
    re_path(r'fbyysite/datamanage/order/upload/taskquery/(\d+)',dmview.orderuploadtaskquery),
    re_path(r'fbyysite/datamanage/storage/upload/taskquery/(\d+)',dmview.storageuploadtaskquery),
    re_path(r'fbyysite/datamanage/store/upload/taskquery/(\d+)',dmview.storeuploadtaskquery),
    re_path(r'fbyysite/taskmanage/pagenum/(\d+)', tmview.taskmanage),
    re_path(r'fbyysite/taskmanage/query/(\d+)',tmview.taskquery),
    path('fbyysite/taskmanage/openbgtaskservice',tmview.startbgtaskservice),
    path('fbyysite/usermanage/visualshow/',umview.user_cal),
    re_path(r'fbyysite/reportmanage/cts/pagenum/(\d+)',rmview.ctsmanage),
    re_path(r'fbyysite/reportmanage/cts/query/(\d+)',rmview.ctsquery),
    path('fbyysite/reportmanage/cts/make',rmview.ctsmake),
    re_path(r'fbyysite/reportmanage/kck/pagenum/(\d+)',rmview.kckmanage),
    re_path(r'fbyysite/reportmanage/kck/ajaxstores?[^/]+',rmview.kck_ajax_store),
    path('fbyysite/reportmanage/kck/add/',rmview.kckadd),
    path('fbyysite/reportmanage/kck/edit/kckeditcheck',rmview.kckeditcheck),
    re_path(r'fbyysite/reportmanage/kck/edit/(.+)',rmview.kckedit),
    path('fbyysite/reportmanage/kck/delete',rmview.kckdel),
]
