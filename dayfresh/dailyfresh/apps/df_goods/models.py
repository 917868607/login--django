from django.db import models

# Create your models here.

# 商品种类的数据模型
class TypeInfo(models.Model):
    
    title = models.CharField(max_length=100,verbose_name='分类名称')
    class_name = models.CharField(max_length=50,default='',verbose_name='')
    type_img  = models.ImageField(upload_to='df_type/%Y/%m/',verbose_name='分类封面图',default='df_type/default.jpg')
    
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        
        return self.title

# 商品信息的数据模型
class GoodInfo(models.Model):

    g_title = models.CharField(max_length=100,verbose_name='商品名称')
    g_pic   = models.ImageField(upload_to='df_goods/%Y/%m',verbose_name='商品图片',default='df_goods/default.jpg')
    # DecimalField() 小数
    g_price = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='商品价格')
    g_unit  = models.CharField(max_length=50,verbose_name='计量单位')
    g_click = models.IntegerField(verbose_name='浏览次数')
    g_desc  = models.CharField(max_length=150,verbose_name='商品描述')
    g_stock = models.IntegerField(verbose_name='库存数量')
    g_content = models.TextField(verbose_name='商品详情')
    
    # 商品与商品类型之间的关系  一对多
    type = models.ForeignKey(TypeInfo,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.g_title
    
    
