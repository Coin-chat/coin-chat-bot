# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-21 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0003_remove_coindb_coin_pirce_kimchi'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Log', models.CharField(max_length=20)),
            ],
        ),
    ]