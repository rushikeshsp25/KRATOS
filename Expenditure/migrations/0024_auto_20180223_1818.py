# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-23 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expenditure', '0023_auto_20180223_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='system',
            name='system_name',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]