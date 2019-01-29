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
from django.contrib import admin
from django.urls import path,re_path
from FileUpload import views as fuview
from SiteLogin import views as slview

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('fbyysite/fileupload',fuview.upload),
    path('fbyysite/login',slview.login),
    path('fbyysite/registe',slview.registe),
    re_path(r'fbyysite/registe/ajaxstores?[^/]+',slview.registe_ajax_store),
    path('fbyysite/index',slview.requires_login(slview.index)),
    path('fbyysite/about',slview.requires_login(slview.about)),
    re_path(r'fbyysite/active/(.*)',slview.activeaccount),
    re_path(r'fbyysite/jump/(.*)',slview.tmpjump),
    path('fbyysite/index/left',slview.index_left),
    path('fbyysite/index/content',slview.index_content),
    path('fbyysite/index/usermanage',slview.index_content),
]
