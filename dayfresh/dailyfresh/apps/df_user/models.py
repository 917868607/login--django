from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    
    address = models.CharField(max_length=200,null=True,verbose_name='收货地址')
    
    postcode = models.CharField(max_length=6,null=True,verbose_name='验证码')
    
    phone = models.CharField(max_length=11,null=True,verbose_name='手机号码')
    
    
