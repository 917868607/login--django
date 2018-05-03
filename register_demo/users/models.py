from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.


# 定义自己数据模型

class UsersModels(AbstractUser):
    # 添加需要的字段，
    # 昵称
    nick_name = models.CharField(max_length=20,verbose_name='昵称',default='')
    # 生日
    #blank=True 表示表单的数据可以为空，默认
    birday = models.DateField(verbose_name='生日',null=True,blank=True)
    # 手机号
    phone = models.CharField(max_length=11,verbose_name='手机号',default='')
    # 地址
    address = models.CharField(max_length=20,verbose_name='地址',default='')
    # 头像
    image = models.ImageField(upload_to='images/%Y/%m',default='images/default.png')
    # 性别 #choices 表示只能两个选择一个
    sex = models.CharField(max_length=20,verbose_name='性别',choices=(('man','男'),('women','女')))

    class Meta:
        db_table = 'users'
        # 后台管理
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

 # 邮箱验证类
class EmailModels(models.Model):

    # 验证码
    code = models.CharField(verbose_name='验证码',max_length=20)
    # 接受用户的邮箱
    email = models.CharField(verbose_name='收件人',max_length=20)
    # 发送时间
    send_time = models.DateField(max_length=20,verbose_name='发送时间')
    # 过期时间
    overtime = models.DateField(max_length=20,verbose_name='过期时间')
    # 邮件类型 1 注册邮件 2 找回密码邮件
    # choices 选项，只能其中选择一个
    send_type = models.CharField(choices=(('register','注册邮件'),('forget','找回密码')),max_length=20)
    class Meta:
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name