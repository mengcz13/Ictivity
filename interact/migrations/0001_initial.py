# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 11:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('timeL', models.DateTimeField()),
                ('timeR', models.DateTimeField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signs', to='activity.Activity')),
                ('users', models.ManyToManyField(related_name='signs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]