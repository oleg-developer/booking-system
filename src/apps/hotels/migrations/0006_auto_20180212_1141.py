# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-12 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_auto_20180209_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='building',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='building'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='bunk_bed',
            field=models.PositiveIntegerField(default=0, verbose_name='bunk bed count'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='double_bed',
            field=models.PositiveIntegerField(default=0, verbose_name='double bed count'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='floor',
            field=models.IntegerField(default=1, verbose_name='floor'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='number_group',
            field=models.CharField(default='', max_length=16, verbose_name='number_group'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='photo'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='single_bed',
            field=models.PositiveIntegerField(default=0, verbose_name='single bed count'),
        ),
    ]
