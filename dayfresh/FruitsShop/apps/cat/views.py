from django.shortcuts import render,HttpResponse,redirect
from django.http.response import JsonResponse
from django.contrib.auth.views import login_required

from django.views import View
# Create your views here.
from fruits.models import *


class AddCart(View):
    def get(self,request):
        pass

    def post(self,request):
        result = {}
        if request.user.is_authenticated:

            good_id = request.POST.get('good_id',None)
            num = request.POST.get('num',None)
            stock = request.POST.get('stock')
            s_money = request.POST.get('s_money')
            if good_id and num:
                cart = ShopCat.objects.filter(comm_id=good_id,user=request.user)
                if cart:
                    if (cart[0].s_num + int(num)) > int(stock):
                        cart[0].s_num = stock
                    else:
                        cart[0].s_num = cart[0].s_num + int(num)
                        cart[0].s_money = cart[0].s_money + float(s_money)
                    cart = cart[0]
                else:
                    cart = ShopCat(comm_id=good_id,user=request.user,s_num=num,s_money= s_money)
                cart.save()
                result['status']=1
                result['Meg'] = '购物车添加成功'
            else:
                result['status'] = 0
                result['Meg'] = '购物车添加失败'
            result['count'] = ShopCat.objects.filter(user=request.user).count()
        else:
            next_href = request.POST.get('next_href')
            next_href = next_href.split('8000')[1]
            result['status'] = 0
            result['Meg'] = '请先登录'
            result['url'] = 'http://127.0.0.1:8000/user/login/?next={}'.format(next_href)
        return JsonResponse(result)


class CartInfo(View):
    def get(self,request):
        result = {}
        if request.user.is_authenticated:
            user = request.user
            carts = ShopCat.objects.filter(user=user)
            result['carts'] = carts
            result['type'] = 'cart'
            return render(request,'df_cart/cart.html',result)
        else:
            return redirect('/user/login/')
        #     next_href = request.POST.get('next_href')
        #     next_href = next_href.split('8000')[1]
        #     result['status'] = 0
        #     result['Meg'] = '请先登录'
        #     result['url'] = 'http://127.0.0.1:8000/user/login/?next={}'.format(next_href)
        # return JsonResponse(result)
    def post(self,request):
        pass


def order_check(request):
    if request.method == 'POST':
        result = {}
        goods_id = request.POST.get('goods_id',None)
        num = request.POST.get('num',None)
        if goods_id and num:
            try:
                cart = ShopCat.objects.get(comm_id=goods_id)
                cart.s_num = num
                cart.save()
                result['status'] = 1
                result['Meg'] = '修改成功'
            except Exception as e:
                result['status'] = 0
                result['Meg'] = '修改失败'
            return JsonResponse(result)
        else:
            return HttpResponse(status=404)

def delete(request):
    if request.method=='GET':
        result = {}
        good_id = request.GET.get('id')
        try:
            ShopCat.objects.get(comm_id=good_id).delete()
            result['status'] = 1
            result['Meg'] = '删除成功'

        except Exception as e:
            result['status'] = 0
            result['Meg'] = '删除失败,网络原因,请刷新页面'
        return JsonResponse(result)
