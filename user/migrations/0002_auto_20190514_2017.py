# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-14 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('female', '女'), ('man', '男')], max_length=20, verbose_name='性别'),
        ),
    ]
