# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 07:22
from __future__ import unicode_literals

import apps.auth_core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('key', models.CharField(default=apps.auth_core.utils.generate_string, editable=False, max_length=128, primary_key=True, serialize=False, verbose_name='key')),
                ('platform', models.SlugField(choices=[('web', 'Web'), ('ios', 'IOS'), ('android', 'Android')], default='web', verbose_name='platform')),
                ('version', models.FloatField(default=1.0, verbose_name='version')),
                ('client', models.CharField(default='', max_length=1024, verbose_name='client')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'auth token',
                'verbose_name_plural': 'auth tokens',
            },
        ),
    ]
