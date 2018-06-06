from django.db import models

from df_user.models import UserProfile
from df_goods.models import GoodInfo

# Create your models here.

class OrderInfo(models.Model):
    o_id   = models.CharField(max_length=100,primary_key=True,verbose_name='订单编号')
    o_date = models.DateTimeField(auto_now_add=True,verbose_name='订单日期')
    o_pay  = models.BooleanField(choices=((True,'已支付'),(False,'未支付')),default=False,verbose_name='是否支付')
    o_total_price = models.CharField(max_length=100,verbose_name='订单总额')
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    
    class Meta:
        
        verbose_name = '订单'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        
        return self.o_id

class OrderDetailInfo(models.Model):

    count = models.IntegerField(verbose_name='商品数量')
    
    goods = models.ForeignKey(GoodInfo,on_delete=models.CASCADE,verbose_name='商品')
    
    order = models.ForeignKey(OrderInfo,on_delete=models.CASCADE,verbose_name='订单')
    
    class Meta:
        
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.goods.g_title

