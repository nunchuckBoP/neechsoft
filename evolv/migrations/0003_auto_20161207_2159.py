# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 21:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('evolv', '0002_auto_20161207_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='followup',
            field=models.DateField(default=datetime.datetime(2016, 12, 14, 21, 59, 26, 332509, tzinfo=utc), verbose_name='Follow up Date'),
        ),
    ]
