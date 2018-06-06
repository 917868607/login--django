from django.shortcuts import render
from django.contrib.auth.views import login_required
from django.http import JsonResponse
from .models import CartInfo
# Create your views here.

@login_required
def cart(request):
    
    if request.method == 'GET':
        # 找到登录用户购物车所有信息
        all_cart = CartInfo.objects.filter(user=request.user)
        context = {
            'title':'天天生鲜-我的购物车',
            'all_cart':all_cart,
            'type':'cart'
        }
        
        return render(request,'df_cart/cart.html',context)


def add_cart(request):
    
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            
            # 取出商品id 商品数
            try:
                g_id = request.POST.get('g_id')
                count = request.POST.get('count')
                # 判断商品是否已经在用户的购物车中,如果在,增加数量,如果不在,创建保存
                try:
                    cart = CartInfo.objects.get(goods_id=g_id,user=request.user)
                except Exception as e:
                    # 没有找到商品
                    cart = CartInfo(goods_id=g_id, count=count, user=request.user)
                else:
                    # 修改商品数据
                    cart.count += int(count)
                # 保存商品购物车记录
                cart.save()
                
            except Exception as e:
                print(e)
                return JsonResponse({
                    'status':2,
                    'msg':'加入购物车失败'
                })
            else:
                return JsonResponse({
                    'status':1,
                    'msg':'加入购物车成功',
                    'count':CartInfo.objects.filter(user=request.user).count()
                })
            
        else:
            next_href = request.POST.get('next_href')
            next_href = next_href.split('8000')[1]
            return JsonResponse({
                'errMsg':'请先登录',
                'url':'/user/login/?next={}'.format(next_href),
                'status':0
            })
    
    
# 查询登录用户的购物车商品数
def query_count(request):
    if request.method == 'GET':
        # 判断用户是否登录
        if request.user.is_authenticated:
            # 查询登录用户的购物车商品数
            count = CartInfo.objects.filter(user=request.user).count()
            return JsonResponse({
                'status':1,
                'count':count
            })
        else:
            return JsonResponse({
                'status':1,
                'count':0
            })

@login_required
def update(request):
    
    if request.method == 'GET':
        
        c_id = request.GET.get('c_id')
        count = request.GET.get('count')
        try:
            cart = CartInfo.objects.get(id=c_id)
            cart.count = count
            cart.save()
        except Exception as e:
            print(e)
            return JsonResponse({
                'status':0,
                'msg':'添加数量失败'
            })
        else:
            return JsonResponse({
                'status':1,
                'msg':'添加成功',
                'count':cart.count
            })
            
        
# 删除购物车
def delete(request):
    if request.method == 'GET':
        c_id = request.GET.get('c_id')
        try:
            cart = CartInfo.objects.get(id=c_id)
            cart.delete()
        except Exception as e:
            
            return JsonResponse({
                'status':0,
                'msg':'删除失败'
            })
        else:
            return JsonResponse({
                'status':1,
                'msg':'删除成功'
            })
    
    
    
        





