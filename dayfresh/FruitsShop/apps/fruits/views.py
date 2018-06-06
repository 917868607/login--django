from django.shortcuts import render
from django.views import View
from .models import *
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.views.generic import ListView

# Create your views here.

def index(request):
    """
    分类
    :param request:
    :return:
    """
    dict = {}
    resp = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']
    types = CommType.objects.all().order_by('id')
    for key, value in enumerate(types):
        dict[(resp[key])] = value
    res = {}
    for ty in types:
        res[ty.class_name] = ty.comminfo_set.all()[:4]
    """
    水果 obj obj obj obj 
    """
    user = request.user
    types = CommType.objects.all()
    result = {'types':dict,'goods':res}
    result['type'] = 'user'
    return render(request,'df_goods/index.html',result)

def lists(request):
    """
    type_id 商品分类
    p=?页面
    :param request: type_id  p=? type 默认 价格
    :return:
    """
    if request.method=='GET':
        dict = {}
        resp = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']
        type_id = request.GET.get('type_id')
        page_num = request.GET.get('p','1')
        comms = CommInfo.objects.filter(type_id=type_id).order_by('?')[:2]
        # 分页
        # 默认 default
        type = request.GET.get('type', 'default')
        if type == 'default':
            adds = CommInfo.objects.filter(type_id=type_id)
        elif type == 'price':
            adds = CommInfo.objects.filter(type_id=type_id).order_by('-c_price')
        elif type == 'hot':
            adds = CommInfo.objects.filter(type_id=type_id).order_by('-c_click')
        paginator = Paginator(adds,3)
        page_num = int(page_num)
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e:
            #非整数
            page = paginator.page(1)
        except EmptyPage as e:
            page_num = int(page_num)
            #输出数字的范围
            #两种情况
            # 1 大于获取最后一页
            # 2 小于第一页
            if page_num >= paginator.num_pages:
                page = paginator.page(paginator.num_pages)
            else:
                page = paginator.page(1)
        # #页码
        # 标签
        types = CommType.objects.all().order_by('id')
        for key,value in enumerate(types):
            dict[resp[key]] = value

        result = {'comms':comms,'page':page,'types':dict,'type':type}
        result['type'] = 'goods'
        return render(request,'df_goods/list.html',result)

class ListsView(ListView):
    goods = CommInfo.objects.all()
    context_object_name = 'lists'
    paginate_by = 3
    template_name = 'df_goods/list.html'

class Detail(View):
    def get(self,request):
        dict = {}
        result = {}
        res = ['fruit','seafood','meet','egg','vegetables','ice']
        com_id = request.GET.get('com_id')
        good = CommInfo.objects.get(id=com_id)
        good.c_click += 1
        good.save()
        comm = CommInfo.objects.get(id=com_id)
        tags = CommTags.objects.filter(comminfo=comm)
        types = CommType.objects.all().order_by('id')
        for key,value in enumerate(types):
            dict[(res[key])] = value
        # 新品推荐
        goods  = comm.type.comminfo_set.order_by('-id')[:2]
        if request.user.id:
            count = ShopCat.objects.filter(user=request.user).count()
            result['count'] = count
        result['com'] = comm
        result['tags'] = tags
        result['types'] = dict
        result['comms'] = goods
        result['type'] = 'goods'

        return render(request,'df_goods/detail.html',result)
    def post(self,request):
        pass

