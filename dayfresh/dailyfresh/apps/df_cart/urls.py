from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$',cart,name='cart_idx'),
    url(r'^add_cart/$',add_cart,name='cart_add'),
    url(r'^query_count',query_count,name='query_count'),
    url(r'^update/$',update,name='cart_update'),
    url(r'^delete/$',delete,name='cart_delete'),
]