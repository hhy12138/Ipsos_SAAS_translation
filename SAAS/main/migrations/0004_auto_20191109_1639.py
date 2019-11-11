# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-09 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191109_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='origin_files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=128)),
                ('status', models.IntegerField()),
                ('progress', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='translated_files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_filename', models.CharField(max_length=128)),
                ('target_filename', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=128)),
            ],
        ),
        migrations.DeleteModel(
            name='translate_files',
        ),
    ]