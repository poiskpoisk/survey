# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveyapp', '0003_auto_20161117_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='qs_single_choice',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No'), ('D', 'Depends')], default='Y', max_length=1, verbose_name='Single choices'),
        ),
    ]
