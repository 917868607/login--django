from django.shortcuts import render, HttpResponse,redirect
from users.models import *

# Create your views here.
from django.views import View
from django.http import JsonResponse
from .froms import *
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.backends import ModelBackend
from fruits.models import *
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage

# Create your views here.

def center(request):
    if request.method == 'GET':
        result = {}
        user = request.user
        orders = CommOrders.objects.filter(user=user)
        #分页
        page = Paginator(orders,4)
        result['orders'] = orders
        result['type'] = 'center'
        return render(request,'df_user/user_center_order.html',result)

def centerinfo(request):
    result = {}


    result['type'] = 'centerinfo'

    return render(request,'df_user/user_center_info.html',result)


def centersize(request):
    if request.method == 'GET':
        result = {}

        result['type'] = 'centersize'
        return render(request, 'df_user/user_center_site.html',result)
    elif request.method =='POST':
        result ={}
        username = request.POST.get('username')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        user = FruitsUsers.objects.get(id=request.user.id)
        user.u_name = username
        user.address = address
        user.postcode = postcode
        user.phone = phone
        user.save()
        result['type'] = 'centerinfo'
        return render(request, 'df_user/user_center_info.html', result)


class RegisterUser(View):
    def get(self, request):
        return render(request, 'df_user/register.html')

    def post(self, request):
        pass


class LoginUser(View):
    def get(self, request):
        return render(request, 'df_user/login.html')

    def post(self, request):
        form = CheckForm(request.POST)
        next = request.GET.get('next')
        if form.is_valid():
            username = form.cleaned_data['user_name']
            pwd = form.cleaned_data['pwd']
            # 判断用户是否存在
            res = FruitsUsers.objects.filter(Q(username=username) | Q(email=username))
            if res:
                user = authenticate(request, username=username, password=pwd)
                if user:
                    login(request, user)
                    status = 1
                    Meg = {'err': '登录成功'}
                    name = 1
                    next = next
                else:
                    status = 0
                    Meg = {'err': '账号密码错误'}
                    name = "pwd"
                    next = None
                result = {'status': status, 'Meg': Meg, 'name': name,'next':next}
                return JsonResponse(result)
            else:
                status = 0
                Meg = {'err': '该用户尚未注册'}
                name = 'username'
            result = {'status': status, 'Meg': Meg, 'name': name}
            return JsonResponse(result)
        else:
            result = {'status': 0, 'Meg': form.errors, 'name': 0}
            return JsonResponse(result)


def checkinfo(request):
    """
    status 0 有错 1 成功
    Meg{'err':信息}
    :param request:
    :return:
    """
    if request.method == "POST":
        form = CheckForm(request.POST)
        if form.is_valid():
            # 判断昵称,email是否存在
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd']
            cpwd = form.cleaned_data['cpwd']
            if FruitsUsers.objects.filter(username=user_name):
                status = 0
                Meg = {'err': '该昵称已经存在'}
                name = 'user_name'
            else:
                if FruitsUsers.objects.filter(email=email):
                    status = 0
                    Meg = {'err': '该邮箱已经注册'}
                    name = 'email'
                else:
                    if pwd != cpwd:
                        status = 0
                        Meg = {'err': '两次密码不一致'}
                        name = 'cpwd'
                    else:
                        user = FruitsUsers(username=user_name, email=email, is_active=1, is_staff=1,
                                           password=make_password(cpwd))
                        user.save()
                        status = 1
                        Meg = {'err': '注册成功'}
                        name = None
            result = {'status': status, 'Meg': Meg, 'name': name}
            return JsonResponse(result)


        else:
            status = 0
            Meg = form.errors
            return JsonResponse({'status': status, 'Meg': Meg, 'name': 0})
    elif request.method == "GET":
        user_name = request.GET.get('user_name', None)
        email = request.GET.get('email', None)
        cpwd = request.GET.get('cpwd', None)
        pwd = request.GET.get('pwd', None)
        if user_name or email:
            user = FruitsUsers.objects.filter(username=user_name)
            email = FruitsUsers.objects.filter(email=email)
            if user or email:
                if email:
                    Meg = {'err': '邮箱已经存在'}
                elif user:
                    Meg = {'err': '用户名已经存在'}
                status = 0
            else:
                if not user:
                    Meg = {'err': '用户可以使用'}
                elif not email:
                    Meg = {'err': '邮箱可以使用'}
                status = 1
            if user_name:
                res = 'user_name'
            else:
                res = 'email'
            result = {'status': status, 'Meg': Meg, 'name': res}
            return JsonResponse(result)
        elif cpwd:
            if cpwd == pwd:
                status = 1
                Meg = {'err': '两次密码一致'}
            else:
                status = 0
                Meg = {'err': '两次密码不一致'}
            res = 'cpwd'
            result = {'status': status, 'Meg': Meg, 'name': res}
            return JsonResponse(result)
        else:
            result = None
            return JsonResponse(result)


def checklogin(request):
    """
    name 0 数据不合法
    status 0 1
    Meg={'err':''}
    :param request:
    :return:
 """
    if request.method == 'GET':
        username = request.GET.get('username', None)
        if username:
            user = FruitsUsers.objects.filter(Q(email=username) | Q(username=username))
            if user:
                status = 1
                Meg = {'err': '用户可以用'}
            else:
                status = 0
                Meg = {'err': '账号密码错误'}
            result = {'status': status, 'Meg': Meg}
            return JsonResponse(result)


        else:
            return HttpResponse(status=404)


class CheckUserAuth(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        username = username
        password = password
        try:
            user = FruitsUsers.objects.get(Q(username=username) | Q(email=username))
            if user:
                if user.check_password(password):
                    return user
                else:
                    None
            else:
                return None
        except Exception as e:
            return None

def logoutuser(request):
    if request.user.id:
        logout(request)
        return redirect('/')
    else:
        return HttpResponse(status=404)
