# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^detail/',Detail.as_view(),name='detail'),
    url(r'^list/',lists,name='list'),
    # url(r'^list/',ListsView.as_view(),name='list')
]