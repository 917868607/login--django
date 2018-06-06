from django.shortcuts import render,redirect
from django.http import JsonResponse
from fruits.models import *
from datetime import datetime
from alipay import AliPay
from FruitsShop import settings
import os


# Create your views here.

def add_order(request):
    if request.method == 'POST':
        result = {}
        if request.user.id:
            cartlist = request.POST.getlist('cartlist[]')
            o_money = request.POST.get('o_money',None)
            if len(cartlist)==1 and len(cartlist[0]) > 12:
                order = CommOrders.objects.get(o_id=cartlist[0])
                result['status'] = 1
                result['Meg'] = '订单提交成功'
            # 生产订单号
            else:
                order = CommOrders()
                order.o_id = '{}{}'.format(datetime.now().strftime('%Y%m%H%M%S'),request.user.id)
                order.user = request.user
                order.o_money = o_money
                order.o_type = False
                order.save()
                for id in cartlist:
                    try:
                        cart = ShopCat.objects.get(id=id)
                        orderinfo = OrderInfo(content=cart.s_num,comm=cart.comm,order=order)
                        orderinfo.save()
                        cart.delete()
                        result['status'] = 1
                        result['Meg'] = '订单提交成功'
                    except Exception as e:
                        result['status'] = 0
                        result['Meg'] = '网络延迟,请重新提交,或刷新网页'
                        return JsonResponse(result)
            # 创键用于支付宝的对象
            ali_pay = AliPay(
                appid= settings.ALIPAY_APPID,
                app_private_key_path=os.path.join(settings.BASE_DIR,'keys/private'),
                alipay_public_key_path=os.path.join(settings.BASE_DIR,'keys/public'),
                app_notify_url=None,
                sign_type='RSA2',
                # 沙箱测试 False,生产True
                debug=False

            )
            # 网站端的支付需要跳转的支付页面,执行支付
            ##http://openapi.alipaydev.com/qateway.do?order=
            order_string = ali_pay.api_alipay_trade_page_pay(
                # 定单号
                out_trade_no=order.o_id,
                #订单总额
                total_amount= order.o_money,
                # 订单描述信息
                subject='天天生鲜购物单-{}'.format(order.o_id),
                return_url='http://www.zhihu.com'
            )
            # 拼接支付地址
            url= settings.ALIPAY_URL + '?'+ order_string
            # 将数据返回前端,前端跳转支付界面
            result['url'] = url
            result['o_id'] = order.o_id
            return JsonResponse(result)
        else:
            result['status'] = 300
            return JsonResponse(result)
    if request.method == 'GET':
        # good_id = request.GET.get('good_id')
        pass

def order(request):

    if request.method =="POST":
        result = {}
        res = request.POST.getlist('cartid')
        cart_list = [ShopCat.objects.get(comm_id=x) for x in request.POST.getlist('cartid')]
        result['title'] = '天天生鲜-提交订单'
        result['type'] = 'goods'
        result['cart_list'] = cart_list
        return render(request,'df_order/place_order.html',result)

    elif request.method == 'GET':
        result = {}
        o_id = request.GET.get('o_id',None)
        if o_id:
            try:
                orders = CommOrders.objects.get(o_id=o_id)
            except Exception as e:
                return redirect('/')
        else:
            return redirect('/')
        result['title'] = '天天生鲜-提交订单'
        result['type'] = 'goods'
        result['orders'] = orders
        result['cart_list'] = None

        return render(request,'df_order/place_order.html',result)


def check_pay(request):
    if request.method == 'GET':
        result = {}
        o_id = request.GET.get('o_id')
        alipy = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR,'keys/private'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR,('keys/public')),
            sign_type='RSA2',
            debug=True
        )
        while True:


            response = alipy.api_alipay_trade_query(o_id)
            code = response.get('code')
            trade_status = response.get('trade_status')
            print(response)
            if code == '10000' and trade_status == 'TRADE_SUCCESS':
                order = CommOrders.objects.get(o_id=o_id)
                orderinfos = order.orderinfo_set.all()
                order.o_type = True
                order.save()
                for orderinfo in orderinfos:
                    #减掉库存
                    comm = CommInfo.objects.get(id=orderinfo.comm_id)
                    if int(comm.c_stock) - int(orderinfo.content) >0:
                        comm.c_stock = int(comm.c_stock) - int(orderinfo.content)
                    else:
                        comm.delete()
                    comm.save()

                return JsonResponse({
                    'status':1,
                    'msg':'支付成功'
                })
            elif(code == '10000' and trade_status=='WAIT_BUYER_PAY') or code =='40004':
                continue
            else:
                return JsonResponse({
                    'status':0,
                    'msg':'交易失败'
                })

