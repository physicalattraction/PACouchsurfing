# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('public_name', models.CharField(max_length=64)),
                ('public_address', models.CharField(max_length=256, default='', blank=True)),
                ('avatar_url', models.URLField(null=True, default='', blank=True)),
                ('is_verified', models.BooleanField()),
                ('is_deleted', models.BooleanField()),
            ],
        ),
    ]
