from django.db import models
from users.models import FruitsUsers
from DjangoUeditor.models import UEditorField


# Create your models here.


# 商品名称
class CommInfo(models.Model):
    c_name = models.CharField(max_length=20, verbose_name='商品名称', null=False)
    c_price = models.FloatField(verbose_name='商品价格', null=False)
    c_comfrom = models.CharField(max_length=100, verbose_name='商品产地')
    c_images = models.ImageField(upload_to='df_goods/', default='df_goods/fruit.jpg', verbose_name='商品图片')
    c_unit = models.CharField(max_length=50,verbose_name='单位/斤')
    c_desc = models.CharField(max_length=255,verbose_name='诱惑')
    # c_stock = models.IntegerField(verbose_name='未知,int')
    type = models.ForeignKey('CommType', on_delete=models.CASCADE, verbose_name='商品分类')
    tags = models.ManyToManyField('CommTags', verbose_name='商品标签')
    # 水果描述
    # c_content = models.TextField(verbose_name='商品描述')
    c_content = UEditorField(
        verbose_name='商品描述',
        width=600,
        height=300,
        toolbars='full',
        imagePath='ueditor/',
        filePath='files/',
        upload_settings={'imagesMaxSize':12040000},
        default=''
    )
    # 库存
    c_stock = models.IntegerField(verbose_name='商品库存')
    c_click = models.IntegerField(verbose_name='商品点击率')

    class Meta:
        db_table = 'commodity'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.c_name)


# 购物车
class ShopCat(models.Model):
    user = models.ForeignKey(FruitsUsers,on_delete=models.CASCADE, verbose_name='用户')
    comm = models.ForeignKey(CommInfo, on_delete=models.CASCADE, verbose_name='商品种类')
    s_num = models.IntegerField(verbose_name='购买的数量')
    s_money = models.FloatField(verbose_name='商品总价')
    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.s_num)


# 商品分类(水果,蔬菜)
class CommType(models.Model):

    class_name = models.CharField(max_length=50, verbose_name='商品分类')
    type_img = models.ImageField(upload_to='df_type/', verbose_name='商品分类图片')

    class Meta:
        db_table = 'type'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.class_name)


# 商品标签(热销)
class CommTags(models.Model):

    tags = models.CharField(max_length=20, verbose_name='商品标签')

    class Meta:
        db_table = 'tags'
        verbose_name = '商品标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.tags)


# 订单表
class CommOrders(models.Model):
    user = models.ForeignKey(FruitsUsers, on_delete=models.CASCADE, verbose_name='用户')
    # 订单号
    o_id = models.CharField(max_length=50,verbose_name='订单号',primary_key=True)
    # 订单时间
    o_date = models.DateTimeField(auto_now_add=True, verbose_name='订单时间')
    # 总价
    o_money = models.CharField(max_length=200, verbose_name='订单价格')
    o_type = models.BooleanField(choices=((True,'已支付'),(False,'未支付')))

    class Meta:
        db_table = 'orders'
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.o_id)


# 订单详情
class OrderInfo(models.Model):
    comm = models.ForeignKey(CommInfo, on_delete=models.CASCADE, verbose_name='订单商品')
    order = models.ForeignKey(CommOrders, on_delete=models.CASCADE, verbose_name='订单')
    content = models.CharField(max_length=255, verbose_name='订单商品数量')

    class Meta:
        db_table = 'orderinfo'
        verbose_name = '订单详情表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.comm)
