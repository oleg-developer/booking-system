# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-26 12:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('users', '0009_auto_20180126_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='chief',
            name='phone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.Phone'),
        ),
        migrations.AddField(
            model_name='staff',
            name='phone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.Phone'),
        ),
    ]
