from django.db import models
from django.utils import timezone

WEATHER_CODE = (
(0, '-'),
(1, 'füst'), (2, 'homály'), (3, 'párásság'), (4, 'köd'), (19, 'nyílt köd'), (13, 'homokvihar'), (14, 'porforgatag'), 
(5, '22-es halo'), (6, 'melléknap'), (7, 'érintő ív'), (8, 'ritkább halo'),
(9, 'villámlás'), (10, 'dörgés'), (11, 'szivárvány'), (12, 'csapadéksáv'),
(15, 'szitálás'), (16, 'szemcsés hó'), (17, 'ónos szitálás'), (34, 'ónos eső'),
(18, 'eső'), (20, 'havazás'), (22, 'havas eső'),
(24, 'zápor'), (25, 'hózápor'), (26, 'havas eső zápor'), (27, 'jégeső'),
(29, 'tuba'), (30, 'tornádó'), (31, 'zivatar'), (32, 'hódara-zápor'), (33, 'fagyott eső'),
(34, 'harmat'), (35, 'dér'), (36, 'zúzmara'), (37, 'hófúvás')
)

class Site(models.Model):
	NARROW_AREA = (
		(1, 'kert'),
		(2, 'parkoló'),
		(3, 'tető'),
		(4, 'udvar'),
		(5, 'füves terület'),
		(6, 'fás terület'),
		(7, 'vízpart'),
		(8, 'utca')
	)

	WIDE_AREA = (
		(1, 'belváros'),
		(2, 'kertváros'),
		(3, 'lakótelep'),
		(4, 'ipari terület'),
		(5, 'hegyvidék'),
		(6, 'vízpart'),
		(7, 'külterület')
	)

	id = models.AutoField(primary_key = True)
	owner = models.ForeignKey('auth.user')
	title = models.CharField(max_length = 100, unique = True)
	comment = models.TextField(blank = True)
	createdDate = models.DateTimeField(default = timezone.now)
	isActive = models.BooleanField(default = True)
	isPublic = models.BooleanField(default = True)
	isDeleted = models.BooleanField(default = False)
	lat = models.DecimalField(max_digits = 20, decimal_places = 15)
	lon = models.DecimalField(max_digits = 20, decimal_places = 15)
	narrowArea = models.IntegerField(choices = NARROW_AREA, default = 1)
	wideArea = models.IntegerField(choices = WIDE_AREA, default = 1) # site.wideArea; site.get_wideArea_display() https://docs.djangoproject.com/en/1.9/topics/db/models/#field-options
	
	def __str__(self):
		return self.title

class Instrument(models.Model):
	id = models.AutoField(primary_key = True)
	siteId = models.ForeignKey('climate.Site')
	type = models.CharField(max_length = 50)
	priority = models.IntegerField(default = 5)
	isActive = models.BooleanField(default = True)
	# milyen szenzor van
	# melyik szenzor mikor uzemelt

class RawData(models.Model):
	siteId = models.ForeignKey('climate.Site')
	instrumentId = models.ForeignKey('climate.Instrument')
	createdDate = models.DateTimeField()
	# T, Rh, p, stb
	# vagy relacios tablaval

class RawObservation(models.Model):
	siteId = models.ForeignKey('climate.Site')
	createdDate = models.DateTimeField(default = timezone.now())
	comment = models.TextField(blank = True)
	weatherCode = models.IntegerField(choices = WEATHER_CODE, default = 0)
	# jelenseg kezdete es vege ?

class RawManualData(models.Model):
	siteId = models.ForeignKey('climate.Site')
	date = models.DateField()
	# Tmin, Tmax, csapadek, jelensegek
	
class DailyStat(models.Model):
	siteId = models.ForeignKey('climate.Site')
	date = models.DateField()

class MonthlyStat(models.Model):
	siteId = models.ForeignKey('climate.Site')
	date = models.DateField()