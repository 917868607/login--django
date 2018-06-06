# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^centerinfo/',centerinfo,name='centerinfo'),
    url(r'^centersize/',centersize,name='centersize'),
    url(r'^center/',center,name='center'),
    url(r'logout/',logoutuser,name='logout'),
    url(r'^checklogin/',checklogin,name='checklogin'),
    url(r'^checkuser/',checkinfo,name='checkuser'),
    url(r'^register/',RegisterUser.as_view(),name='register'),
    url(r'^login/',LoginUser.as_view(),name='login')
]