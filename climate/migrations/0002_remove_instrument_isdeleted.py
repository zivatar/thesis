# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-05 15:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrument',
            name='isDeleted',
        ),
    ]