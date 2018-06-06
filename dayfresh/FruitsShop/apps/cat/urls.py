# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^order_check/',order_check,name='order_check'),
    url(r'^delete/',delete,name='delete'),
    url(r'^cartinfo/',CartInfo.as_view(),name='cart_info'),
    url(r'^add_cart/',AddCart.as_view(),name='add_cart'),
]