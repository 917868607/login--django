from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import login,logout,login_required

# Create your views here.
from .models import UserProfile


def mylogin(request):

    if request.method == 'GET':
        
        return render(request,'df_user/login.html')
    elif request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')
        context = {}
        if UserProfile.objects.filter(username=username):
        
            user = UserProfile.objects.get(username=username)
            
            if user.check_password(password):
                
                context['status'] = 1
                context['msg'] = '登录成功'
                context['next'] = request.GET.get('next','')
                login(request,user)
            else:
                context['satus'] = 0
                context['msg'] = '账户或密码错误'
        else:
            context['status'] = 0
            context['msg'] = '用户不存在'
        
        
        return JsonResponse(context)
            
        
        
 
@login_required
def register(request):
    
    if request.method == 'GET':
        
        return render(request,'df_user/register.html')
    
    elif request.method == 'POST':
        
        # 取出用户名 密码 邮箱
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        context = {}
        
        if UserProfile.objects.filter(username=username):
            context['status'] = 0
            context['msg'] = '该用户已存在,请重新输入用户名'
            return JsonResponse(context)
        else:
            
            try:
                user = UserProfile(username=username,
                                   password=make_password(password),
                                   email=email)
                user.save()
            except Exception as e:
                
                print(e)
                return JsonResponse({
                    'status':500,
                    'msg':'您的网络不稳定,注册失败,请稍后重试!'
                })
            else:
                return JsonResponse({
                    'status':200,
                    'msg':'注册成功'
                })
                
            
            
        
        
def mylogout(request):
    
    logout(request)
    
    return redirect('/goods/')
        
        
        
        
    
# 判断用户是否存在
def check_user(request):

    if request.method == 'GET':
        username = request.GET.get('username')
        # 判断用户是否存在
        if UserProfile.objects.filter(username=username):
            
            return JsonResponse({
                'status':0,
                'msg':"该用户名已被占用,请换个名字。"
            })
        else:
            
            return JsonResponse({
                'status':1,
                'msg':'恭喜您,该用户名可以使用!'
            })
        
        
        
    
    
    
    
    