from django.db import models
from django.utils import timezone
import calendar
import datetime
import decimal
import simplejson as json

monthList = ['J', 'F', 'M', 'Á', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']

class Weather(models.Model):
	WEATHER_CODE = (
	(1, 'füst'), (2, 'homály'), (3, 'párásság'), (4, 'köd'), (19, 'nyílt köd'), (13, 'homokvihar'), (14, 'porforgatag'), 
	(5, '22-es halo'), (6, 'melléknap'), (7, 'érintő ív'), (8, 'ritkább halo'),
	(9, 'villámlás'), (10, 'dörgés'), (11, 'szivárvány'), (12, 'csapadéksáv'),
	(15, 'szitálás'), (16, 'szemcsés hó'), (17, 'ónos szitálás'), (34, 'ónos eső'),
	(18, 'eső'), (20, 'havazás'), (22, 'havas eső'),
	(24, 'zápor'), (25, 'hózápor'), (26, 'havas eső zápor'), (27, 'jégeső'),
	(29, 'tuba'), (30, 'tornádó'), (31, 'zivatar'), (32, 'hódara-zápor'), (33, 'fagyott eső'),
	(34, 'harmat'), (35, 'dér'), (36, 'zúzmara'), (37, 'hófúvás')
	)

	BEAUFORT_SCALE = (
	(-1, 'nem észlelt'),
	(0, '0: szélcsend'), (1, '1: füst lengedezik'), (2, '2: arcon érezhető'), (3, '3: vékony gallyak mozognak'),
	(4, '4: kisebb ágak mozognak'), (5, '5: nagyobb ágak mozognak, suhog'), (6, '6: drótkötelek zúgnak, vastag ágak mozognak'),
	(7, '7: gallyak letörnek'), (8, '8: ágak letörnek'), (9, '9: gyengébb fák kidőlnek, épületekben kisebb károk'),
	(10, '10: fák gyökerestül kidőlnek'), (11, '11: súlyos károk'), (12, '12: súlyos pusztítás')
	)
	
	def getWeatherCodeText(self, ndx):
		if type(ndx) == str and ndx != '':
			ndx = int(ndx)
		find = [x[1] for x in self.WEATHER_CODE if x[0] == ndx]
		if len(find) > 0:
			return find[0]
		
class Month:
	def __init__(self, now=timezone.now(), year=0, month=0):
		if year == 0 or month == 0:
			self.year = now.year
			self.month = now.month
		else:
			self.year = int(year)
			self.month = int(month)
		print(type(self.month))
	def isInMonth(self, dt):
		return self.year == dt.year and self.month == dt.month
	def daysOfMonth(self):
		lastDay = calendar.monthrange(self.year, self.month)[1]
		print(lastDay)
		a = []
		[a.append(i) for i in range(1, lastDay + 1)]
		return a
	def daysOfMonthTillToday(self):
		lastDay = timezone.now().day
		a = []
		[a.append(i) for i in range(1, lastDay + 1)]
		return a
	def getMonth(self):
		return str(self.month).zfill(2) 

class Climate:
	def getNrFrostDays(self, minTemps):
		return [len(x for x in minTemps if x < 0)]
	def getNrColdDays(self, minTemps):
		return [len(x for x in minTemps if x < -10)]
	def getNrWarmNights(self, minTemps):
		return [len(x for x in minTemps if x > 20)]
	def getNrSummerDays(self, maxTemps):
		return [len(x for x in maxTemps if x > 25)]
	def getNrWarmDays(self, maxTemps):
		return [len(x for x in maxTemps if x >= 30)]
	def getNrHotDays(self, maxTemps):
		return [len(x for x in maxTemps if x >= 35)]
		
# -----------------------------------------------------------------------------------------

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
	createdDate = models.DateTimeField(default = timezone.now())
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
	class Meta:
		unique_together = (('siteId', 'createdDate'),)
	
	siteId = models.ForeignKey('climate.Site')
	createdDate = models.DateTimeField()
	pressure = models.DecimalField(blank = True, null = True, max_digits = 5, decimal_places = 1)
	tempIn = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	humidityIn = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	temperature = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	humidity = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	dewpoint = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	windChill = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	windSpeed = models.DecimalField(blank = True, null = True, max_digits = 4, decimal_places = 1)
	windDir = models.DecimalField(blank = True, null = True, max_digits = 4, decimal_places = 1)
	gust = models.DecimalField(blank = True, null = True, max_digits = 4, decimal_places = 1)
	precipitation = models.DecimalField(blank = True, null = True, max_digits = 4, decimal_places = 1)
	
	#def __init__(self, siteId, createdDate):
	#	self.siteId = siteId
	#	self.createdDate = createdDate
	
class DailyStatistics(models.Model):
	class Meta:
		unique_together = (('siteId', 'date'),)
	siteId = models.ForeignKey('climate.Site', primary_key = True)
	date = models.DateTimeField()
	dataAvailable = models.IntegerField(default = 0)
	tempMin = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	tempMax = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	tempAvg = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	precipitation = models.DecimalField(blank = True, null = True, max_digits = 4, decimal_places = 1)
	precipHalfHour = models.DecimalField(blank = True, null = True, max_digits = 4, decimal_places = 1)

class MonthlyStatistics(models.Model):
	class Meta:
		unique_together = (('year', 'month', 'siteId'),)
	siteId = models.ForeignKey('climate.Site', primary_key = True)
	year = models.IntegerField()
	month = models.IntegerField()
	dataAvailable = models.IntegerField(default = 0)
	tempMin = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	tempMax = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	tempAvg = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	summerDays = models.IntegerField()

class YearlyStatistics(models.Model):
	class Meta:
		unique_together = (('siteId', 'year'),)
	siteId = models.ForeignKey('climate.Site', primary_key = True)
	year = models.IntegerField()

class MonthlyReport():
	class Meta:
		managed = False
	def generateTemperatures(self):
		Tavg = []
		Tmin = []
		Tmax = []
		for i in self.days:
			hasData = False
			for j in self.dayObjs:
				if j.date.day == i:
					Tavg.append(j.tempAvg)
					Tmin.append(j.tempMin)
					Tmax.append(j.tempMax)
			if not hasData:
				Tmin.append(None)
				Tmax.append(None)
				Tavg.append(None)
		return json.dumps(Tmin), json.dumps(Tavg), json.dumps(Tmax)
	def __init__(self, siteId, year, month, monthObjs, yearObj, dayObjs):
		self.siteId = siteId
		self.year = year
		self.month = month
		self.monthObjs = monthObjs
		self.yearObj = yearObj
		self.dayObjs = dayObjs
		self.days = Month(year=self.year, month=self.month).daysOfMonth()
		self.tempMins, self.tempAvgs, self.tempMaxs = self.generateTemperatures()
	
	
class RawObservation(models.Model):
	siteId = models.ForeignKey('climate.Site')
	createdDate = models.DateTimeField(default = timezone.now())
	comment = models.TextField(blank = True)
	_weatherCode = models.CommaSeparatedIntegerField(max_length = 200, choices = Weather.WEATHER_CODE, blank = True)
	windSpeed = models.IntegerField(choices = Weather.BEAUFORT_SCALE, default = 0)
	# jelenség regisztrálása a statisztikákba
	def populateWeatherCode(self, arr):
		wc = ''
		for a in arr:
			wc = wc + a + ','
		self._weatherCode = wc
		self.save()
	@property
	def weatherCode(self):
		return self.convertToReadables(self._weatherCode.split(','))
		#return self._weatherCode.split(',')
	@weatherCode.setter
	def weatherCode(self, value):
		self._weatherCode = value
	def convertToReadables(self, codes):
		out = []
		for o in codes:
			out.append(self.convertToReadable(o))
		return out
	def convertToReadable(self, code):
		return Weather.getWeatherCodeText(Weather(), code)

class RawManualData(models.Model):
	siteId = models.ForeignKey('climate.Site')
	year = models.IntegerField(default = -1)
	month = models.IntegerField(default = -1) # TODO year,month,siteId legyen unique
	day = models.IntegerField(default = -1)
	tMin = models.FloatField(blank = True, null = True)
	tMax = models.FloatField(blank = True, null = True)
	precAmount = models.FloatField(blank = True, null = True)
	_weatherCode = models.CommaSeparatedIntegerField(max_length = 200, choices = Weather.WEATHER_CODE, blank = True)
	def populateWeatherCode(self, arr):
		wc = ''
		for a in arr:
			wc = wc + a + ','
		self._weatherCode = wc
		self.save()
	@property
	def weatherCode(self):
		return self._weatherCode.split(',')
	@weatherCode.setter
	def weatherCode(self, value):
		self._weatherCode = value
	
class DailyStat(models.Model):
	siteId = models.ForeignKey('climate.Site')
	date = models.DateField()

class MonthlyStat(models.Model):
	siteId = models.ForeignKey('climate.Site')
	date = models.DateField()

class YearlyReport(models.Model):
	siteId = models.ForeignKey('climate.Site')
	year = models.IntegerField(default = -1)