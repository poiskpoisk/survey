# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveyapp', '0004_auto_20161117_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='user_ans_multy',
            field=models.ManyToManyField(blank=True, to='surveyapp.MultipleChoicesQS'),
        ),
    ]
