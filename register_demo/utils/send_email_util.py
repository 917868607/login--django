# -*- coding: utf-8 -*-

from django.core.mail import send_mail
import random
import datetime
from register_demo import settings
from users.models import EmailModels

# 随机生成验证码
def codes(lenght=16):
    strs = 'qwertpoiuytasdfghjklzxcvbnmQWERTYUIOPSDFGHJKLZXCVBNM123456789'

    code =''
    for x in range(lenght):
        code += random.choice(strs)

    return code

# 发送邮件
def send_email(to_email,send_type='register'):

    email = EmailModels()
    # 获取验证码
    email.code = codes()
    #收件人
    email.email = to_email
    # 设置时间验证邮件过期时间
    email.send_time = datetime.datetime.now()
    #设置邮件是三天后过期
    email.overtime = datetime.datetime.now()+ datetime.timedelta(days=3)
    # 邮件类型
    email.send_type = send_type
    email.save()
    try:
        if send_type=='register':
            look = '欢迎注册cctv开心网'
            html_message = '<a href="http://127.0.0.1:8000/users/active_email/{}">点击此处http://192.168.12.242:8000/users/active_email/{}验证激活cctv开心网，开启快乐之旅</a>'.format(email.code,email.code)
        else:
            look = '修改密码'
            html_message = '<a href="http://127.0.0.1:8000/users/ame_password/{}">点击此处http://192.168.12.242:8000/users/ame_password/{}激活连接，修改密码</a>'.format(email.code,email.code)
        res = send_mail(look,'',settings.EMAIL_HOST_USER,[to_email],html_message=html_message)

    except EmailModels as e:
        return False
    else:
        if res:
            return True
        else:
            return False