from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$',goods,name='goods_idx'),
    url(r'^list/$',goodslist,name='goods_list'),
    url(r'^detail/$',goodsdetail,name='goods_detail'),
]