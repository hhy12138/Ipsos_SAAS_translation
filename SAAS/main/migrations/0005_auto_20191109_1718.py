# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-09 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20191109_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='origin_files',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]