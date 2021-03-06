# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-05 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0008_auto_20171227_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpbitDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_name', models.CharField(max_length=30)),
                ('coin_price', models.FloatField()),
                ('check_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_key', models.CharField(max_length=30)),
                ('exchange_name', models.CharField(max_length=15)),
                ('coin_name', models.CharField(max_length=30)),
                ('coin_price', models.FloatField()),
                ('coin_count', models.FloatField(blank=True)),
            ],
        ),
    ]
