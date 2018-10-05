# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/14 15:55'
from users.models import EmailVerifyRecord
from secrets import randbelow

from django.core.mail import send_mail

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
    email_rec.save()
    if send_type == 'register':
        email_title = '在线教育平台注册激活链接'
        email_body = '请点击下面的链接激活您的账号： http://127.0.0.1:8000/activate/' + email_rec.code
    elif send_type == 'forget':
        email_title = '在线教育平台找回密码链接'
        email_body = '请点击下面的链接重置您的密码： http://127.0.0.1:8000/reset/' + email_rec.code

    send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM,
                            recipient_list=[receiver], auth_user=EMAIL_HOST_USER, auth_password=EMAIL_HOST_PASSWORD)
    #1 发送成功   0 发送失败
    if send_status == 1:
        pass
