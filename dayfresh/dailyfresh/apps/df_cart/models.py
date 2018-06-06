from django.db import models
from df_user.models import UserProfile
from df_goods.models import GoodInfo
# Create your models here.

class CartInfo(models.Model):
    
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户')
    goods = models.ForeignKey(GoodInfo,on_delete=models.CASCADE,verbose_name='商品')
    count = models.IntegerField(verbose_name='数量')