# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-21 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expenditure', '0015_auto_20180221_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='debits',
            name='remarks',
            field=models.TextField(blank=True),
        ),
    ]
