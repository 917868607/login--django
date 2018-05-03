# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import RegisterView,LoginView,Active_email,Amend_pd,Ame_password,AlterPassword,Center,Logot,Modify,Update
from django.views.static import serve
from register_demo import settings
urlpatterns = [
    url(r'^media/(?P<path>\w+)',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
    url(r'^update/',Update.as_view(),name='update'),
    url(r'^modify_center/',Modify.as_view(),name='modify_center'),
    url(r'^logout/',Logot.as_view(),name='logout'),
    url(r'^center/', Center.as_view(),name='center'),
    url(r'^alterpasswd/$',AlterPassword.as_view(),name='alterpasswd'),
    url(r'^ame_password/(?P<code>\w+)',Ame_password.as_view()),
    url(r'amend_pd/$',Amend_pd.as_view(),name='amend_pd'),
    url(r'active_email/(?P<code>\w+)',Active_email.as_view()),
    url(r'^login/',LoginView.as_view(),name='login'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
]