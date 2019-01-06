# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/10/9 7:58'

from django import template

from utils.aliyun_manager import videoManager


register = template.Library()
@register.simple_tag
def relative_url(field_name, value, urlencode=None):
    url = f"?{field_name}={value}"
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = f"{url}&{encoded_querystring}"
    return url


@register.simple_tag
def get_video_url(video_path, expires=3600):
    return videoManager.get_video_url(video_path, expires)
