# Generated by Django 2.1.5 on 2019-02-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_auto_20190210_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=models.TextField(default='', verbose_name='课程详情'),
        ),
    ]