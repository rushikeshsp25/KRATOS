# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-13 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Expenditure', '0028_auto_20180313_2214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balence',
            old_name='balence',
            new_name='current_balence',
        ),
        migrations.AddField(
            model_name='balence',
            name='event',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='Expenditure.Event', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='balence',
            name='total_balence',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
