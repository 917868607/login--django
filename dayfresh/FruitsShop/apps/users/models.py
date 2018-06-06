from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class FruitsUsers(AbstractUser):
    address = models.CharField(max_length=200,default='中国',verbose_name='地址')
    phone = models.CharField(max_length=11,blank=True,default=110,verbose_name='电话')
    postcode = models.CharField(max_length=6,verbose_name='邮编')
    u_name = models.CharField(max_length=50,verbose_name='收件人',default='小花')
    class Meta:
        db_table = 'users'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

# 邮箱验证
class CheckEmail(models.Model):
    email = models.EmailField(verbose_name='注册邮箱')
    code = models.CharField(max_length=100,verbose_name='验证码')
    send_time = models.DateTimeField(auto_now_add=True,verbose_name='发送时间')
    over_time = models.DateTimeField(verbose_name='过期时间')
    email_type = models.CharField(max_length=25,choices=(('login','登录'),('register','注册')),verbose_name='邮箱类型')
    #是否已经激活
    email_actiate = models.BooleanField(choices=((True,'已经激活'),(False,'没有激活')),verbose_name='激活状态')
    class Meta:
        db_table = 'email'
        verbose_name = '验证邮箱'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.email)