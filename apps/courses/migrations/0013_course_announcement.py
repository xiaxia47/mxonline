# Generated by Django 2.1 on 2018-12-22 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20181219_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='announcement',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='课程公告'),
        ),
    ]
