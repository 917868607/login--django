from django import template

register = template.Library()

@register.filter
def key(d,key):
    # 返回根据key取出的列表
    return d[key]