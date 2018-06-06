from datetime import datetime
import os
from django.shortcuts import render
from django.contrib.auth.views import login_required
from django.http import JsonResponse
from alipay import AliPay

# Create your views here.
from df_cart.models import CartInfo
from .models import OrderInfo,OrderDetailInfo
from df_goods.models import GoodInfo
from dailyfresh import settings
@login_required
def order(request):
    """
    订单
    :param request:
    :return:
    """
    if request.method == 'POST':
        cart_list = [CartInfo.objects.get(id=c_id) for c_id in request.POST.getlist('cartid')]
        context = {
            'title':'天天生鲜-提交订单',
            'type':'goods',
            'cart_list':cart_list
        }
        return render(request,'df_order/place_order.html',context)
@login_required
def add_order(request):
    if request.method =='POST':
        cartlist = request.POST.getlist('cartlist[]')
        total_price = request.POST.get('total_price')

        #创建订单

        order = OrderInfo()
        #订单编号 时间201805252044156
        # strftime('%Y%m%H%M%S')编码格式
        order.o_id = '{}{}'.format(datetime.now().strftime('%Y%m%H%M%S'),request.user.id)
        order.user = request.user
        order.o_total_price = total_price
        order.save()
        #将商品储存订单储存订单详情表
        for x in cartlist:
            cart = CartInfo.objects.get(id=x)
            order_detail = OrderDetailInfo()
            order_detail.goods = cart.goods
            order_detail.order = order
            order_detail.count = cart.count
            order_detail.save()
            #订单信息和订单详情保存后,删除购物车中的商品
            cart.delete()
        #创建用于支付宝的对象
        ali_pay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,#使用默认回调的地址
            alipay_public_key_path=os.path.join(settings.BASE_DIR,'keys/public'),
            app_private_key_path=os.path.join(settings.BASE_DIR,'keys/private'),
            #使用的加密方式
            sign_type='RSA2',
            #默认是Flase  测试环境配合沙箱环境使用  如果是的生产环境 将改为True
            debug=False
        )
        #网站端的支付需要跳转到的支付页面,执行支付
        #http://openapi.alipaydev.com/qateway.do?order=
        order_string = ali_pay.api_alipay_trade_page_pay(
            #订单号
            out_trade_no=order.o_id,
            #订单总额
            total_amount=total_price,
            #订单描述信息
            subject='天天生鲜购物单-{}'.format(order.o_id),
            #回调地址,订单支付成功后回调地址
            return_url='https://www.baidu.com',
        )
        #拼接支付地址
        url = settings.ALIPAY_URL + '?'+order_string
        #将数据返回给前端,前段跳转到支付界面支付
        result={'status':1,'msg':'请求成功','url':url,'o_id':order.o_id}
        return JsonResponse(result)
# 监测订单是否支付
def check_pay(request):
    if request.method == 'GET':
        o_id = request.GET.get('o_id')
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR,'keys/pri'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR,'keys/pub'),
            sign_type='RSA2',
            # 沙箱环境下没有查询订单服务的
            debug=True
        )
        
        while True:
            response = alipay.api_alipay_trade_query(o_id)
            # code 40004 支付订单未创建
            # code 10000 trade_status  WAIT_BUYER_PAY  等待支付
            # oode 10000 trade_status  TRADE_SUCCESS  支付成功
        
            # response 是字典
            code = response.get('code')
            trade_status =response.get('trade_status')

            if code == '10000' and trade_status == 'TRADE_SUCCESS':
                # 支付成功
                # 返回支付结果
                return JsonResponse({
                    'status':1,
                    'msg':'支付成功'
                })
            elif (code == '10000' and trade_status =='WAIT_BUYER_PAY') or code == '40004':
                # 表示支付暂时没有完成
                continue
            else:
                return JsonResponse({
                    'status':0,
                    'msg':'支付失败'
                })

             
            
    
        



