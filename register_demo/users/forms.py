# -*- coding: utf-8 -*-
from django import forms

from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': '请输入正确的邮箱'})
    nick_name = forms.CharField(required=True)
    password = forms.CharField(max_length=6, required=True, error_messages={'invalid': '密码不得少于6位'})
    repassword = forms.CharField(max_length=6, required=True, error_messages={'invalid': '密码不得少于6位'})
    captcha = CaptchaField(required=True, error_messages={'invalid': '请输入正确的验证码'})


class LoginFrom(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': '请输入正确的邮箱'})
    password = forms.CharField(max_length=6, required=True, error_messages={'invalid': '密码不得少于6位'})
    captcha = CaptchaField(required=True, error_messages={'invalid': '请输入正确的验证码'})


class Amend_pd(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': '请输入正确的邮箱'})
    captcha = CaptchaField(required=True, error_messages={'invalid': '请输入正确的验证码'})


class Alterpasswd(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': '请输入正确的邮箱'})
    password = forms.CharField(max_length=6, required=True, error_messages={'invalid': '密码不得少于6位'})
    repassword = forms.CharField(max_length=6, required=True, error_messages={'invalid': '密码不得少于6位'})
