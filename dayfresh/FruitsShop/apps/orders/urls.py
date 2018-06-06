# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',order,name='order'),
    url(r'^checkorder/',check_pay,name='checkorder'),
    url(r'add_order/',add_order,name='add_order')
]