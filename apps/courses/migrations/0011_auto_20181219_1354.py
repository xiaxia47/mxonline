# Generated by Django 2.1 on 2018-12-19 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20181218_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='instructions',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='introduction',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='老师引言'),
        ),
    ]
