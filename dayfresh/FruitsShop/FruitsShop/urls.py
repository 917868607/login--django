"""FruitsShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from FruitsShop import settings
from fruits.views import index
import xadmin


urlpatterns = [
    url(r'^cart/',include('cat.urls')),
    url(r'^order/',include('orders.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^user/',include('users.urls')),
    url(r'^fruits/',include('fruits.urls')),
    url(r'^$',index,name='index'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
    url(r'^static/(?P<path>.*)',serve,{'document_root':settings.STATIC_ROOT},name='static'),
    url(r'^xadmin/', xadmin.site.urls),
]
