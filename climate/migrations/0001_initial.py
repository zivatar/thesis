# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime(2017, 2, 24, 21, 20, 46, 161177, tzinfo=utc))),
                ('isActive', models.BooleanField(default=True)),
                ('isPublic', models.BooleanField(default=True)),
                ('lat', models.DecimalField(max_digits=9, decimal_places=6)),
                ('lon', models.DecimalField(max_digits=9, decimal_places=6)),
                ('narrowArea', models.IntegerField(default=1, choices=[(1, 'kert'), (2, 'parkoló')])),
                ('wideArea', models.IntegerField(default=1, choices=[(1, 'belváros'), (2, 'kertváros'), (3, 'lakótelep')])),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
