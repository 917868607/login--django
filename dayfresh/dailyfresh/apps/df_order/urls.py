from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$',order,name='order_idx'),
    url(r'^add_order/$',add_order,name='add_order'),
    url(r'^check_pay/$',check_pay,name='check_pay'),
]