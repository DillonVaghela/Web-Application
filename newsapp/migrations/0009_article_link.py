# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-10 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='link',
            field=models.TextField(default='link', max_length=10000),
            preserve_default=False,
        ),
    ]
