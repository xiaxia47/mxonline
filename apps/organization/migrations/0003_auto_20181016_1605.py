# Generated by Django 2.1 on 2018-10-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_courseorg_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name=''),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=0, verbose_name='修习人数'),
        ),
    ]
