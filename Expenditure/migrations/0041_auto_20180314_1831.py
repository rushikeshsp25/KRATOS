# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-14 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Expenditure', '0040_auto_20180314_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credits',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Expenditure.Event'),
        ),
    ]
