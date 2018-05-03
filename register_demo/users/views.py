from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from django.views import View
from .forms import RegisterForm, LoginFrom
from .forms import Amend_pd as Amend_password, Alterpasswd
from .models import UsersModels, EmailModels
from utils.send_email_util import send_email
# 密码加密
from django.contrib.auth.hashers import make_password
import datetime
import time
# 引入login 函数,自动记录session
from django.contrib.auth import login as logins, logout
from django.contrib.auth import authenticate
# 利用内置的检查模块
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 判断昵称是否已经存在
            email = form.cleaned_data['email']
            # 判断是不是已经注册过
            if not UsersModels.objects.filter(email=email):
                nick_name = form.cleaned_data['nick_name']
                users = UsersModels.objects.filter(nick_name=nick_name)
                if not users:
                    password = form.cleaned_data['password']
                    repassword = form.cleaned_data['repassword']
                    if form.cleaned_data['password'] == form.cleaned_data['repassword']:
                        # users = UsersModels(nick_name=nick_name,password=password)
                        # 发送邮件
                        res = send_email(email, send_type='register')
                        if res:
                            mg = UsersModels(email=email, password=make_password(password), nick_name=nick_name,
                                             username=email)
                            mg.save()
                            return HttpResponse('邮件验证发送成功')
                        else:
                            return HttpResponse('邮件发送失败')
                    else:
                        return render(request, 'register.html', {'form': form, 'error': '两次密码不一样请重新输入'})
                else:
                    return render(request, 'register.html', {'form': form, 'errMeg': '该用户已经存在请重新填写！'})
            else:
                return render(request, 'register.html', {'form': form, 'error': '该用户已注册，请检查邮箱地址/登录'})
        else:
            return render(request, 'register.html', {'form': form})
class LoginView(View):
    def get(self, request):
        form = LoginFrom()
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = LoginFrom(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # 判断用户是否存在
            res = UsersModels.objects.filter(email=email)
            if res:
                # 判断该用户密码是否正确
                # 直接使用user.password == password 肯定是不通过的
                # 需要对密码加密后再判断
                # user = UserProfile.objects.get(email=email,password=make_password(password))
                # 1.用户名 2.密码
                # authenticate 会对password进行加密后再对比
                # 如果正好密码匹配返回这个user对象,如果不匹配返回None
                # 判断密码是否正确
                user = authenticate(request=request, username=email, password=password)
                if user:
                    # 利用login函数
                    logins(request, user)
                    return redirect('index')
                else:
                    # 密码错误
                    return render(request, 'login.html', {'form': form, 'errMsg': '账号或密码错误，请仔细检查'})
            else:
                # 用户不存在
                return render(request, 'login.html', {'form': form, 'errMsg': '该用户不存在，请检查邮箱'})
        else:
            return render(request, 'login.html', {"form": form})
class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        return HttpResponse('这是post请求到主页')
class Active_email(View):

    def get(self, request, code):
        # 判断验证码是否正确
        if EmailModels.objects.filter(code=code):
            # 判断是否失效
            now = datetime.datetime.now()
            # 转换为时间戳
            now_time = time.mktime(now.timetuple())
            email = EmailModels.objects.get(code=code)
            over_time = email.overtime
            over_time = time.mktime(over_time.timetuple())
            if now_time < over_time:
                form = LoginFrom()
                return render(request, 'login.html', {'form': form})

        return HttpResponse('<a href="http://127.0.0.1:8000/users/register">验证码已失效，请点击重新注册</a>')

    def post(self):
        return redirect('index')
# 注册验证码
class Amend_pd(View):
    def get(self, request):
        form = Amend_password()
        return render(request, 'amend_passwd.html', {'form': form})

    def post(self, request):

        form = Amend_password(request.POST)
        if form.is_valid():
            # 判断是否是已存在邮箱
            email = UsersModels.objects.filter(email=form.cleaned_data['email'])
            if email:
                # 发送邮件
                res = send_email(email[0].email, send_type='forget')
                if res:
                    return HttpResponse('修改密码邮件发送成功')
                else:
                    return HttpResponse('修改密码邮件发送失败')
            else:
                return render(request, {"form": form, 'error': '该账户尚未注册请检查后重试'})
        else:
            return render(request, 'amend_passwd.html', {'form': form})
# 修改密码验证码
class Ame_password(View):
    def get(self, request, code):
        # 判断验证码
        if EmailModels.objects.filter(code=code):
            # 判断是否失效
            now = datetime.datetime.now()
            # 转换为时间戳
            now_time = time.mktime(now.timetuple())
            email = EmailModels.objects.get(code=code)
            over_time = email.overtime
            over_time = time.mktime(over_time.timetuple())
            if now_time < over_time:
                email = email.email
                return render(request, 'writer_passwd.html', {"email": email})
        return HttpResponse('<a href="http://127.0.0.1:8000/users/register">验证码已失效，请点击重新注册</a>')

    def post(self, request):
        return redirect('index')
# 修改密码
class AlterPassword(View):

    def get(self, request):
        return redirect('index')

    def post(self, request):
        form = Alterpasswd(request.POST)
        print(form)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        repassword = form.cleaned_data['repassword']
        if form.is_valid():
            if password == repassword:
                mg = UsersModels.objects.get(email=email)
                mg.password = make_password(password)
                mg.save()
                return HttpResponse('<a href="http://127.0.0.1:8000/">密码修改成功，密码是{}，点击重新登录</a>'.format(password))
            else:
                return render(request, 'writer_passwd.html', {'form': form, 'error': '密码不一致，请仔细检查'})
        else:
            return render(request, 'writer_passwd.html', {'form': form})
class Center(View):
    def get(self,request):
        return render(request,'center.html')
    def post(self,request):
        return redirect('index')
class Logot(View):
    def get(self,request):
        logout(request)
        return redirect('index')
    def post(self,request):
        pass
class Modify(View):
    def get(self,request):
        return render(request,'modify_center.html')
    def post(self,request):
        pass
class Update(View):
    def get(self, request):
        return redirect('index')

    def post(self, request):
        nick_name = request.POST.get('nick_name')
        birday = request.POST.get('birday','')
        phone = request.POST.get('phone','')
        sex = request.POST.get('optionsRadios')
        mg = UsersModels.objects.get(email=request.user.email)
        mg.nick_name=nick_name
        mg.birday = birday
        mg.phone = phone
        mg.sex = sex
        mg.save()
        return redirect('index')
class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 可以通过email\mobile账号登录
            user = UsersModels.objects.get(Q(email=username) | Q(nick_name=username))
            # check_password 验证用户的密码是否正确
            if user.check_password(password):
                return user
            else:
                if user.password == password:
                    return True
                else:
                    return None
        except Exception as e:
            return None
