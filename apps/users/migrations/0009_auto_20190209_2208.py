# Generated by Django 2.1.5 on 2019-02-09 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190207_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='valid',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='是否有效'),
        ),
    ]
