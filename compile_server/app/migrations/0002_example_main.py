# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_squashed_0004_example_original_dir'),
    ]

    operations = [
        migrations.AddField(
            model_name='example',
            name='main',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
