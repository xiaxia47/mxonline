# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/14 15:55'
from users.models import EmailVerifyRecord
from secrets import randbelow

from django.core.mail import send_mail
from django.shortcuts import reverse
from MxOnline.settings import DOMAIN_URL

from MxOnline.settings import EMAIL_HOST_USER, EMAIL_FROM, EMAIL_HOST_PASSWORD


def email_is_exist(model_name, email):
    if model_name.objects.filter(email=email):
        return True
    else:
        return False


def generate_random_str(random_length=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01234567890'
    random = randbelow
    length = len(chars)
    return "".join([chars[random(length)] for cnt in range(random_length)])


def send_register_email(receiver, send_type='register'):
    email_rec = EmailVerifyRecord()
    email_rec.code = generate_random_str(16)
    email_rec.send_type = send_type
    email_rec.email = receiver
    email_rec.valid = True
    if send_type == 'register':
        email_title = '在线教育平台注册激活链接'
        email_body = (f'请点击下面的链接激活您的账号：{DOMAIN_URL}'
                      f"{reverse('users:activate', kwargs={'active_code': email_rec.code})}")
    elif send_type == 'forget':
        email_title = '在线教育平台找回密码链接'
        email_body = (f'请点击下面的链接重置您的密码：{DOMAIN_URL}' 
                      f"{reverse('users:reset', kwargs={'reset_code': email_rec.code})}")

    send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM,
                            recipient_list=[receiver], auth_user=EMAIL_HOST_USER, auth_password=EMAIL_HOST_PASSWORD)
    #1 发送成功   0 发送失败
    email_rec.send_status = 'succeed' if send_status == 1 else 'failed'
    email_rec.save()

