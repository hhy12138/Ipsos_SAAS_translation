# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-09 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20191109_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='password_validation',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]