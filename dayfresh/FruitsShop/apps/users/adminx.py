# -*- coding: utf-8 -*-

import xadmin
from .models import *
from fruits.models import *
from xadmin import views


class GlobleSettings():
    site_title = '天天生鲜管理系统'
    site_footer = '天天生鲜管理系统, 哈哈版权所有'
    menu_style = 'accordion'
xadmin.site.register(views.CommAdminView,GlobleSettings)

class Basesetings():
    enable_themes = True
    use_bootswath = True
xadmin.site.register(views.BaseAdminView,Basesetings)




class EmailAdmin(object):
    list_display = ['email','code','send_time','over_time','email_type']
    list_filter = ['send_time','over_time']
    search_fields = ['email','code','email_type']
xadmin.site.register(CheckEmail,EmailAdmin)


class ComminfoXadmin():
    list_display = ['c_name', 'c_price', 'c_comfrom', 'c_images', 'c_content','c_click']
    search_fields = ['c_name', 'c_price', 'c_comfrom']

    style_fields = {'c_content':'ueditor'}
xadmin.site.register(CommInfo, ComminfoXadmin)

class CommAdmin():
    list_display = ['tags']
    search_fields = ['tags']

xadmin.site.register(CommTags,CommAdmin)


class ShopCatAdmin():
    list_display = ['user','comm','s_num']
    search_fields = ['user','comm','s_num']
xadmin.site.register(ShopCat,ShopCatAdmin)

class CommOrderAdmin():
    list_display = ['user', 'o_num', 'o_date','o_money']
    search_fields = ['user', 'o_num', 'o_date','o_money']

xadmin.site.register(CommOrders,CommOrderAdmin)

class CommTypeAdmin():
    list_display = ['class_name', 'type_img']
    search_fields = ['class_name', 'type_img']

xadmin.site.register(CommType,CommTypeAdmin)
