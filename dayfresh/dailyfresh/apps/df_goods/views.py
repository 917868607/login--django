from django.shortcuts import render
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from .models import TypeInfo,GoodInfo
# Create your views here.

def goods(request):
    
    context = {}
    # 商品分类
    types = TypeInfo.objects.all()
    goods = {}
    hot_goods = {}
    
    for type in types:
        # 把分类名称作为key,值对应的分类下前四个商品
        goods[type.title] = type.goodinfo_set.all()[:4]
        # 该分类下的人气商品
        hot_goods[type.title] = type.goodinfo_set.all().order_by('-g_click')[:3]

    context['goods'] = goods
    context['hot_goods'] = hot_goods
    context['types'] = types
    # 在前端界面中会判断type从而知道进入的是哪个界面,展示不同的标签
    context['type'] = 'goods'
    
    return render(request,'df_goods/index.html',context)

def goodslist(request):

    if request.method == 'GET':
        context = {}
        t_id = request.GET.get('t_id')
        # 获取分类id及id对应商品
        try:
            TypeInfo.objects.get(id=t_id)
        except Exception as e:
            
            return render(request,'404.html')
        
        # 取出新品推荐的商品
        newsgoods = GoodInfo.objects.filter(type_id=t_id).order_by('-id')[:2]
        # 获取排序方式
        sort_type = request.GET.get('s_type','default')
        # 默认排序
        if sort_type == 'default':
            goods = GoodInfo.objects.filter(type_id=t_id).order_by('-id')
        elif sort_type == 'price':
            goods = GoodInfo.objects.filter(type_id=t_id).order_by('g_price')
        elif sort_type == 'hot':
            goods = GoodInfo.objects.filter(type_id=t_id).order_by('-g_click')
        
        page_num = request.GET.get('p',1)
        pages = Paginator(goods,3)
        try:
            goods = pages.page(page_num)
        except PageNotAnInteger as e:
            goods = pages.page(1)
        except EmptyPage as e:
            goods = pages.page(pages.num_pages)
        
        context['goods'] = goods
        context['newsgoods'] = newsgoods
        context['s_type'] = sort_type
        
        context['type'] = 'goods'
        
        return render(request,'df_goods/list.html',context)

# 商品详情界面
def goodsdetail(request):
    if request.method == 'GET':
        # 取出商品id
        g_id = request.GET.get('g_id')
        # 取出商品
        try:
            good = GoodInfo.objects.get(id=g_id)
        except Exception as e:
            
            return render(request,'404.html')
        else:
            # 浏览次数+1
            good.g_click +=1
            good.save()
            # 获取商品对应类型的商品集合,排序 取俩
            newsgoods = good.type.goodinfo_set.order_by('-id')[:2]
            
            context = {
                'title':'天天生鲜-{}'.format(good.g_title),
                'type':'goods',
                'good':good,
                'newsgoods':newsgoods,
            }
        
        return render(request,'df_goods/detail.html',context)



    
    

    