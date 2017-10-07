# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('priority', models.IntegerField(default=5)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('createdDate', models.DateTimeField()),
                ('pressure', models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=1)),
                ('tempIn', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('humidityIn', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('temperature', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('humidity', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('dewpoint', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('windChill', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('windSpeed', models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)),
                ('windDir', models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)),
                ('gust', models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)),
                ('precipitation', models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)),
            ],
        ),
        migrations.CreateModel(
            name='RawManualData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('year', models.IntegerField(default=-1)),
                ('month', models.IntegerField(default=-1)),
                ('day', models.IntegerField(default=-1)),
                ('tMin', models.FloatField(blank=True, null=True)),
                ('tMax', models.FloatField(blank=True, null=True)),
                ('precAmount', models.FloatField(blank=True, null=True)),
                ('_weatherCode', models.CommaSeparatedIntegerField(max_length=200, blank=True, choices=[(1, 'füst'), (2, 'homály'), (3, 'párásság'), (4, 'köd'), (19, 'nyílt köd'), (13, 'homokvihar'), (14, 'porforgatag'), (5, '22-es halo'), (6, 'melléknap'), (7, 'érintő ív'), (8, 'ritkább halo'), (9, 'villámlás'), (10, 'dörgés'), (11, 'szivárvány'), (12, 'csapadéksáv'), (15, 'szitálás'), (16, 'szemcsés hó'), (17, 'ónos szitálás'), (34, 'ónos eső'), (18, 'eső'), (20, 'havazás'), (22, 'havas eső'), (24, 'zápor'), (25, 'hózápor'), (26, 'havas eső zápor'), (27, 'jégeső'), (29, 'tuba'), (30, 'tornádó'), (31, 'zivatar'), (32, 'hódara-zápor'), (33, 'fagyott eső'), (34, 'harmat'), (35, 'dér'), (36, 'zúzmara'), (37, 'hófúvás')])),
            ],
        ),
        migrations.CreateModel(
            name='RawObservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('_weatherCode', models.CommaSeparatedIntegerField(max_length=200, blank=True, choices=[(1, 'füst'), (2, 'homály'), (3, 'párásság'), (4, 'köd'), (19, 'nyílt köd'), (13, 'homokvihar'), (14, 'porforgatag'), (5, '22-es halo'), (6, 'melléknap'), (7, 'érintő ív'), (8, 'ritkább halo'), (9, 'villámlás'), (10, 'dörgés'), (11, 'szivárvány'), (12, 'csapadéksáv'), (15, 'szitálás'), (16, 'szemcsés hó'), (17, 'ónos szitálás'), (34, 'ónos eső'), (18, 'eső'), (20, 'havazás'), (22, 'havas eső'), (24, 'zápor'), (25, 'hózápor'), (26, 'havas eső zápor'), (27, 'jégeső'), (29, 'tuba'), (30, 'tornádó'), (31, 'zivatar'), (32, 'hódara-zápor'), (33, 'fagyott eső'), (34, 'harmat'), (35, 'dér'), (36, 'zúzmara'), (37, 'hófúvás')])),
                ('windSpeed', models.IntegerField(default=0, choices=[(-1, 'nem észlelt'), (0, '0: szélcsend'), (1, '1: füst lengedezik'), (2, '2: arcon érezhető'), (3, '3: vékony gallyak mozognak'), (4, '4: kisebb ágak mozognak'), (5, '5: nagyobb ágak mozognak, suhog'), (6, '6: drótkötelek zúgnak, vastag ágak mozognak'), (7, '7: gallyak letörnek'), (8, '8: ágak letörnek'), (9, '9: gyengébb fák kidőlnek, épületekben kisebb károk'), (10, '10: fák gyökerestül kidőlnek'), (11, '11: súlyos károk'), (12, '12: súlyos pusztítás')])),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('isActive', models.BooleanField(default=True)),
                ('isPublic', models.BooleanField(default=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('lat', models.DecimalField(max_digits=20, decimal_places=15)),
                ('lon', models.DecimalField(max_digits=20, decimal_places=15)),
                ('narrowArea', models.IntegerField(default=1, choices=[(1, 'kert'), (2, 'parkoló'), (3, 'tető'), (4, 'udvar'), (5, 'füves terület'), (6, 'fás terület'), (7, 'vízpart'), (8, 'utca')])),
                ('wideArea', models.IntegerField(default=1, choices=[(1, 'belváros'), (2, 'kertváros'), (3, 'lakótelep'), (4, 'ipari terület'), (5, 'hegyvidék'), (6, 'vízpart'), (7, 'külterület')])),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyStatistics',
            fields=[
                ('siteId', models.ForeignKey(primary_key=True, serialize=False, to='climate.Site')),
                ('date', models.DateTimeField()),
                ('dataAvailable', models.IntegerField(default=0)),
                ('tempMin', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('tempMax', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('tempAvg', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('precipitation', models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)),
                ('precipHalfHour', models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)),
                ('tempDistribution', models.CommaSeparatedIntegerField(max_length=200, blank=True)),
                ('rhDistribution', models.CommaSeparatedIntegerField(max_length=200, blank=True)),
                ('windDistribution', models.CommaSeparatedIntegerField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyStatistics',
            fields=[
                ('siteId', models.ForeignKey(primary_key=True, serialize=False, to='climate.Site')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('dataAvailable', models.IntegerField(default=0)),
                ('tempMin', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('tempMax', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('tempAvg', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('precipitation', models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)),
                ('tempMinAvg', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('tempMaxAvg', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)),
                ('summerDays', models.IntegerField(blank=True, null=True)),
                ('frostDays', models.IntegerField(blank=True, null=True)),
                ('coldDays', models.IntegerField(blank=True, null=True)),
                ('warmNights', models.IntegerField(blank=True, null=True)),
                ('warmDays', models.IntegerField(blank=True, null=True)),
                ('hotDays', models.IntegerField(blank=True, null=True)),
                ('tempDistribution', models.CommaSeparatedIntegerField(max_length=200, blank=True)),
                ('rhDistribution', models.CommaSeparatedIntegerField(max_length=200, blank=True)),
                ('windDistribution', models.CommaSeparatedIntegerField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='YearlyStatistics',
            fields=[
                ('siteId', models.ForeignKey(primary_key=True, serialize=False, to='climate.Site')),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='site',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rawobservation',
            name='siteId',
            field=models.ForeignKey(to='climate.Site'),
        ),
        migrations.AddField(
            model_name='rawmanualdata',
            name='siteId',
            field=models.ForeignKey(to='climate.Site'),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='siteId',
            field=models.ForeignKey(to='climate.Site'),
        ),
        migrations.AddField(
            model_name='monthlystat',
            name='siteId',
            field=models.ForeignKey(to='climate.Site'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='siteId',
            field=models.ForeignKey(to='climate.Site'),
        ),
        migrations.AddField(
            model_name='dailystat',
            name='siteId',
            field=models.ForeignKey(to='climate.Site'),
        ),
        migrations.AlterUniqueTogether(
            name='yearlystatistics',
            unique_together=set([('siteId', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='rawdata',
            unique_together=set([('siteId', 'createdDate')]),
        ),
        migrations.AlterUniqueTogether(
            name='monthlystatistics',
            unique_together=set([('year', 'month', 'siteId')]),
        ),
        migrations.AlterUniqueTogether(
            name='dailystatistics',
            unique_together=set([('siteId', 'date')]),
        ),
    ]
