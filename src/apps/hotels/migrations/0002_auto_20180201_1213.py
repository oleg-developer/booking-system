# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-01 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20180129_1055'),
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distancetype',
            name='name',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='stars',
        ),
        migrations.RemoveField(
            model_name='locationtype',
            name='name',
        ),
        migrations.RemoveField(
            model_name='street',
            name='name',
        ),
        migrations.RemoveField(
            model_name='streettype',
            name='name',
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='', max_length=64, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='distancetype',
            name='label',
            field=models.CharField(default='', max_length=32, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='distancetype',
            name='value',
            field=models.CharField(default='', max_length=32, verbose_name='value'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='chief',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='hotel', to='users.Chief', verbose_name='chief'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='rating',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='rating'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='rating_confirmed',
            field=models.BooleanField(default=False, verbose_name='rating confirmed'),
        ),
        migrations.AddField(
            model_name='locationtype',
            name='label',
            field=models.CharField(default='', max_length=32, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='locationtype',
            name='value',
            field=models.CharField(default='', max_length=32, verbose_name='value'),
        ),
        migrations.AddField(
            model_name='street',
            name='label',
            field=models.CharField(default='', max_length=64, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='streettype',
            name='label',
            field=models.CharField(default='', max_length=32, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='streettype',
            name='value',
            field=models.CharField(default='', max_length=32, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='address',
            name='building',
            field=models.CharField(blank=True, default='', max_length=8, null=True, verbose_name='building'),
        ),
        migrations.AlterField(
            model_name='address',
            name='distance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotel_addresses', to='hotels.Distance', verbose_name='distance'),
        ),
        migrations.AlterField(
            model_name='address',
            name='house',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='house'),
        ),
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='address',
            name='location_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotel_addresses', to='hotels.LocationType', verbose_name='location type'),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='longitude'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotel_addresses', to='hotels.Street', verbose_name='street'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=32, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='registration_from',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='registration from'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='registration_to',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='registration to'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='website',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='website'),
        ),
    ]
