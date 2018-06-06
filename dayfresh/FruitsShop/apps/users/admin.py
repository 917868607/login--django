from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['email','phone','address','postcode']
    list_filter = ['last_login']
    search_fields = ['username','email','phone','postcode']

admin.site.register(FruitsUsers,UserAdmin)

class EmailAdmin(admin.ModelAdmin):
    list_display = ['email','code','send_time','over_time','email_type']
    list_filter = ['send_time','over_time']
    search_fields = ['email','code','email_type']
admin.site.register(CheckEmail,EmailAdmin)
