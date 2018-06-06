# -*- coding: utf-8 -*-

from django.contrib.auth.forms import forms

class CheckForm(forms.Form):
    user_name = forms.CharField(max_length=255)
    pwd =  forms.CharField(max_length=20,min_length=6)
    cpwd = forms.CharField(max_length=20,min_length=6,required=False)
    email = forms.EmailField(required=False)