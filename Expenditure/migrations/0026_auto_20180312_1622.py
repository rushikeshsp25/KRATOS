# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-12 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Expenditure', '0025_event_subevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='credits',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Expenditure.Event'),
        ),
        migrations.AddField(
            model_name='debits',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Expenditure.Event'),
        ),
        migrations.AddField(
            model_name='debits',
            name='subevent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Expenditure.SubEvent'),
        ),
    ]
