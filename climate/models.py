from django.db import models
from django.utils import timezone
import calendar
import datetime
import decimal
import simplejson as json

from .classes.weather import Weather


monthList = ['J', 'F', 'M', 'Á', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']


		
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

class Year:
	def monthsOfYear(self):
		a = []
		[a.append(i) for i in range(1, 13)]
		return a

class Climate(object):
	tempDistribLimits = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
	rhDistribLimits = [20, 40, 60, 80]
	windDirLimits = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]

	def getNrFrostDays(minTemps):
		return len([x for x in minTemps if x != None and x < 0])
	def getNrColdDays(minTemps):
		return len([x for x in minTemps if x != None and x < -10])
	def getNrWarmNights(minTemps):
		return len([x for x in minTemps if x != None and x > 20])
	def getNrSummerDays(maxTemps):
		return len([x for x in maxTemps if x != None and x > 25])
	def getNrWarmDays(maxTemps):
		return len([x for x in maxTemps if x != None and x >= 30])
	def getNrHotDays(maxTemps):
		return len([x for x in maxTemps if x != None and x >= 35])

	@staticmethod
	def calculateDistribution(data, limits):
		res = []
		for i in range(len(limits)):
			if (i == 0):
	  			high = limits[i]
			elif (i == len(limits) - 1):
	  			low = limits[i]
			else:
	  			low = limits[i]
	  			high = limits[i+1]
			sublist = [x for x in data if x != None and (high == None or x <= high) and (low == None or x > low)]
			res.append(len(sublist))
		return res

	@staticmethod
	def calculateTempDistrib(temps):
		data = Climate.calculateDistribution(temps, Climate.tempDistribLimits)
		return data

	@staticmethod
	def calculateRhDistrib(rhs):
		data = Climate.calculateDistribution(rhs, Climate.rhDistribLimits)
		return data

	@staticmethod
	def calculateWindDistrib(rhs):
		data = Climate.calculateDistribution(rhs, Climate.windDirLimits)
		return data
		
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
	createdDate = models.DateTimeField(auto_now_add=True)
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
	tempDistribution = models.CommaSeparatedIntegerField(max_length = 200, blank = True)
	rhDistribution = models.CommaSeparatedIntegerField(max_length = 200, blank = True)
	windDistribution = models.CommaSeparatedIntegerField(max_length = 200, blank = True)

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
	precipitation = models.DecimalField(blank = True, null = True, max_digits = 4, decimal_places = 1)
	tempMinAvg = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	tempMaxAvg = models.DecimalField(blank = True, null = True, max_digits = 3, decimal_places = 1)
	summerDays = models.IntegerField(blank = True, null = True)
	frostDays = models.IntegerField(blank = True, null = True)
	coldDays = models.IntegerField(blank = True, null = True)
	warmNights = models.IntegerField(blank = True, null = True)
	warmDays = models.IntegerField(blank = True, null = True)
	hotDays = models.IntegerField(blank = True, null = True)
	tempDistribution = models.CommaSeparatedIntegerField(max_length = 200, blank = True)
	rhDistribution = models.CommaSeparatedIntegerField(max_length = 200, blank = True)
	windDistribution = models.CommaSeparatedIntegerField(max_length = 200, blank = True)

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
					hasData = True
					Tavg.append(j.tempAvg)
					Tmin.append(j.tempMin)
					Tmax.append(j.tempMax)
			if not hasData:
				Tmin.append(None)
				Tmax.append(None)
				Tavg.append(None)
		return Tmin, Tavg, Tmax
	def getPrecipitation(self):
		prec = []
		precDay = 0
		precDay10 = 0
		precDay30 = 0
		precDay50 = 0
		for i in self.days:
			hasData = False
			for j in self.dayObjs:
				if j.date.day == i:
					hasData = True
					prec.append(j.precipitation)
					precDay = precDay + 1
					if j.precipitation >= 10:
						precDay10 = precDay10 + 1
					if j.precipitation >= 30:
						precDay30 = precDay30 + 1
					if j.precipitation >= 50:
						precDay50 = precDay50 + 1
			if not hasData:
				prec.append(None)
		return prec, { 0: precDay, 10: precDay10, 30: precDay30, 50: precDay50}
	def generateTempDistribution(self):
		dist = []
		for l in range(len(Climate.tempDistribLimits)):
			sublist = []
			for i in self.days:
				hasData = False
				for j in self.dayObjs:
					if j.date.day == i:
						hasData = True
						dailyData = j.tempDistribution
						if dailyData != None and dailyData != "":
							sublist.append(int(float(dailyData.split(',')[l])))
				if not hasData:
					sublist.append(None)
			dist.append(sublist)
		return dist
	def generateRhDistribution(self):
		dist = []
		for l in range(len(Climate.rhDistribLimits)):
			sublist = []
			for i in self.days:
				hasData = False
				for j in self.dayObjs:
					if j.date.day == i:
						hasData = True
						dailyData = j.rhDistribution
						if dailyData != None and dailyData != "":
							sublist.append(int(float(dailyData.split(',')[l])))
				if not hasData:
					sublist.append(None)
			dist.append(sublist)
		return dist
	def generateWindDistribution(self):
		dist = []
		for l in range(len(Climate.windDirLimits)):
			sublist = []
			for i in self.days:
				hasData = False
				for j in self.dayObjs:
					if j.date.day == i:
						hasData = True
						dailyData = j.windDistribution
						if dailyData != None and dailyData != "":
							sublist.append(int(float(dailyData.split(',')[l])))
				if not hasData:
					sublist.append(None)
			dist.append(sublist)
		return dist
	def calculateIndices(self):
		return ({
			'frostDays': Climate.getNrFrostDays(self.tempMins),
			'coldDays': Climate.getNrColdDays(self.tempMins),
			'warmNights': Climate.getNrWarmNights(self.tempMins),
			'summerDays': Climate.getNrSummerDays(self.tempMins),
			'warmDays': Climate.getNrWarmDays(self.tempMins),
			'hotDays': Climate.getNrHotDays(self.tempMins)
			})
	def __init__(self, siteId, year, month, monthObjs, yearObj, dayObjs):
		self.siteId = siteId
		self.year = year
		self.month = month
		self.monthObjs = monthObjs
		self.yearObj = yearObj
		self.dayObjs = dayObjs
		self.days = Month(year=self.year, month=self.month).daysOfMonth()
		self.tempMins, self.tempAvgs, self.tempMaxs = self.generateTemperatures()
		self.indices = self.calculateIndices()
		self.tempMins = json.dumps(self.tempMins)
		self.tempAvgs = json.dumps(self.tempAvgs)
		self.tempMaxs = json.dumps(self.tempMaxs)
		self.tempDist = json.dumps(self.generateTempDistribution())
		self.rhDist = json.dumps(self.generateRhDistribution())
		self.prec, self.precDist = json.dumps(self.getPrecipitation()[0]), self.getPrecipitation()[1]
		self.windDist = json.dumps(self.generateWindDistribution())

class YearlyReport():
	class Meta:
		managed = False
	def collectData(self, prop):
		dataset = []
		for i in self.months:
			hasData = False
			for j in self.monthObjs:
				if j.month == i:
					hasData = True
					dataset.append(getattr(j, prop))
			if not hasData:
				dataset.append(None)
		return dataset
	def generateTempDistribution(self):
		dist = []
		for l in range(len(Climate.tempDistribLimits)):
			sublist = []
			for i in self.months:
				hasData = False
				for j in self.monthObjs:
					if j.month == i:
						hasData = True
						dailyData = j.tempDistribution
						if dailyData != None and dailyData != "":
							sublist.append(int(float(dailyData.split(',')[l])))
				if not hasData:
					sublist.append(None)
			dist.append(sublist)
		return dist
	def generateRhDistribution(self):
		dist = []
		for l in range(len(Climate.rhDistribLimits)):
			sublist = []
			for i in self.months:
				hasData = False
				for j in self.monthObjs:
					if j.month == i:
						hasData = True
						dailyData = j.rhDistribution
						if dailyData != None and dailyData != "":
							sublist.append(int(float(dailyData.split(',')[l])))
				if not hasData:
					sublist.append(None)
			dist.append(sublist)
		return dist
	def generateWindDistribution(self):
		dist = []
		for l in range(len(Climate.windDirLimits)):
			sublist = []
			for i in self.months:
				hasData = False
				for j in self.monthObjs:
					if j.month == i:
						hasData = True
						dailyData = j.windDistribution
						if dailyData != None and dailyData != "":
							sublist.append(int(float(dailyData.split(',')[l])))
				if not hasData:
					sublist.append(None)
			dist.append(sublist)
		return dist
	def __init__(self, siteId, year, monthObjs, yearObj):
		self.siteId = siteId
		self.year = year
		self.monthObjs = monthObjs
		self.yearObj = yearObj
		self.months = Year().monthsOfYear()
		self.temps ={
			'mins': json.dumps(self.collectData('tempMin')),
			'minAvgs': json.dumps(self.collectData('tempMinAvg')),
			'avgs': json.dumps(self.collectData('tempAvg')) ,
			'maxAvgs': json.dumps(self.collectData('tempMaxAvg')),
			'maxs': json.dumps(self.collectData('tempMax'))
		}
		self.tempIndices = {
			'summerDays': json.dumps(self.collectData('summerDays')),
			'frostDays': json.dumps(self.collectData('frostDays')),
			'coldDays': json.dumps(self.collectData('coldDays')),
			'warmNights': json.dumps(self.collectData('warmNights')),
			'warmDays': json.dumps(self.collectData('warmDays')),
			'hotDays': json.dumps(self.collectData('hotDays'))
		}
		self.prec = json.dumps(self.collectData('precipitation'))
		self.tempDist = json.dumps(self.generateTempDistribution())
		self.rhDist = json.dumps(self.generateRhDistribution())
		self.windDist = json.dumps(self.generateWindDistribution())

class RawObservation(models.Model):
	siteId = models.ForeignKey('climate.Site')
	createdDate = models.DateTimeField(auto_now_add=True)
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