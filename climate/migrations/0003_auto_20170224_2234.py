# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0002_auto_20170224_2221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='created_date',
            new_name='createdDate',
        ),
        migrations.AlterField(
            model_name='site',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
