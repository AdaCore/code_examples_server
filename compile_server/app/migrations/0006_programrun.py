# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-19 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_delete_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_dir', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
