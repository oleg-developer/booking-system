# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-24 10:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('users', '0002_auto_20180123_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chief',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Country', verbose_name='country')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'chief',
                'verbose_name_plural': 'chiefs',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Chief', verbose_name='chief')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'manager',
                'verbose_name_plural': 'managers',
            },
        ),
    ]
