# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snapventure', '0011_auto_20161110_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='code',
            field=models.SmallIntegerField(),
        ),
    ]