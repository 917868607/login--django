# -*- coding: utf-8 -*-

from django.contrib.auth.forms import forms
from captcha.fields import CharField



class CheckForm(forms.Form):
    email = forms.EmailField()