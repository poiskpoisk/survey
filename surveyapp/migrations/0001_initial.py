# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 10:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Customer name')),
                ('survey_name', models.CharField(max_length=100, unique=True, verbose_name='Survey name')),
                ('i_file', models.FileField(upload_to='surveyapp/', verbose_name='Input file')),
            ],
            options={
                'verbose_name_plural': 'Customers',
                'verbose_name': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='MultipleChoicesQS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100, verbose_name='Choice')),
            ],
            options={
                'verbose_name_plural': 'Multiple choice questions',
                'verbose_name': 'Multiple choice question',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qs_id', models.PositiveIntegerField(verbose_name='Question ID')),
                ('qs_name', models.CharField(max_length=100, verbose_name='Question name')),
                ('qs_text', models.CharField(max_length=200, verbose_name='Question text')),
                ('qs_type', models.CharField(blank=True, choices=[('S', 'single'), ('M', 'multiple'), ('T', 'string')], max_length=1, null=True, verbose_name='Question type')),
                ('ans_time', models.PositiveIntegerField(blank=True, null=True, verbose_name='Answer_time')),
                ('user_ans', models.CharField(blank=True, max_length=200, null=True, verbose_name='User answer')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveyapp.Customer')),
                ('user_ans_multy', models.ManyToManyField(to='surveyapp.MultipleChoicesQS')),
            ],
            options={
                'verbose_name_plural': 'Surveys',
                'verbose_name': 'Survey',
            },
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together=set([('name', 'survey_name')]),
        ),
    ]
