# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default=''),
        ),
    ]