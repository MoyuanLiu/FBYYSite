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
from FileUpload import views as fuview
from SiteLogin import views as slview
from UserManage import views as umview
from DataManage import views as dmview
from PermissionManage import views as pmview

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('fbyysite/fileupload',fuview.upload),
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
    path('fbyysite/datamanage/product/upload/taskcancel', dmview.productuploadtaskcancel),
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
]
