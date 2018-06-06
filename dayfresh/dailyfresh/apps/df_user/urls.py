from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^login/',mylogin,name='login'),
    url(r'^logout/',mylogout,name='logout'),
    url(r'^register/$',register,name='register'),
    url(r'^check_user/$',check_user,name='check_user'),
    
]