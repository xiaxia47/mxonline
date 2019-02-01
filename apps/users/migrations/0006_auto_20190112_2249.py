# Generated by Django 2.1 on 2019-01-12 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_emailverifyrecord_send_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverifyrecord',
            name='expired',
            field=models.DateTimeField(blank=True, null=True, verbose_name='失效时间'),
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('pincode', '验证码')], max_length=10, verbose_name='验证码类型'),
        ),
    ]
