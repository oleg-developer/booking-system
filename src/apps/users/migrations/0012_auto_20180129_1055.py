# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-29 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20180126_1302'),
        ('users', '0011_access_staffaccess'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chief',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='phone',
        ),
        migrations.AddField(
            model_name='chief',
            name='phones',
            field=models.ManyToManyField(related_name='_chief_phones_+', to='common.Phone', verbose_name='phones'),
        ),
        migrations.AddField(
            model_name='staff',
            name='phones',
            field=models.ManyToManyField(related_name='_staff_phones_+', to='common.Phone', verbose_name='phones'),
        ),
    ]
