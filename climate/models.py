from django.db import models
from django.template.defaultfilters import slugify

import simplejson as json
import os
from picklefield.fields import PickledObjectField

from .classes.weather import Weather
from .classes.month import Month
from .classes.year import Year
from .classes.climate import Climate

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_image_path_site1(instance, filename):
    return os.path.join('uploads', 'site', str(instance.id))


def get_image_path_instrument1(instance, filename):
    return os.path.join('uploads', 'instrument', str(instance.siteId.pk))


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

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.user')
    title = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    isPublic = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    lon = models.DecimalField(max_digits=20, decimal_places=15)
    narrowArea = models.IntegerField(choices=NARROW_AREA, default=1)
    wideArea = models.IntegerField(choices=WIDE_AREA,
                                   default=1)
    primaryImage = models.ImageField(upload_to=get_image_path_site1, blank=True, null=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    canUpload = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Instrument(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.user')
    siteId = models.ForeignKey('climate.Site', blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)
    type = models.CharField(max_length=50)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    primaryImage = models.ImageField(upload_to=get_image_path_instrument1, blank=True, null=True)


class RawData(models.Model):
    class Meta:
        unique_together = (('siteId', 'createdDate'),)

    siteId = models.ForeignKey('climate.Site')
    createdDate = models.DateTimeField()
    pressure = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=1)
    tempIn = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    humidityIn = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    temperature = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    humidity = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    dewpoint = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    windChill = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    windSpeed = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    windDir = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    gust = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    precipitation = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)


class DailyStatistics(models.Model):
    class Meta:
        unique_together = (('siteId', 'year', 'month', 'day'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    dataAvailable = models.IntegerField(default=0)
    tempMin = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempMax = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    precipitation = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    precipHalfHour = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    tempDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    rhDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    windDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)


class MonthlyStatistics(models.Model):
    class Meta:
        unique_together = (('year', 'month', 'siteId'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField()
    month = models.IntegerField()
    dataAvailable = models.IntegerField(default=0)
    tempMin = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempMax = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    precipitation = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    tempMinAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempMaxAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    summerDays = models.IntegerField(blank=True, null=True)
    frostDays = models.IntegerField(blank=True, null=True)
    coldDays = models.IntegerField(blank=True, null=True)
    warmNights = models.IntegerField(blank=True, null=True)
    warmDays = models.IntegerField(blank=True, null=True)
    hotDays = models.IntegerField(blank=True, null=True)
    tempDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    rhDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    windDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    significants = PickledObjectField(default={})


class YearlyStatistics(models.Model):
    class Meta:
        unique_together = (('siteId', 'year'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField()
    significants = PickledObjectField(default={})


class Report():
    def getNrOfSnowDays(self):
        s = 0
        for j in self.manualDayObjs:
            if j.isSnow:
                s = s + 1
        return s


class MonthlyReport(Report):
    class Meta:
        managed = False

    def generateTemperatures(self):
        Tavg = []
        Tmin = []
        Tmax = []
        for i in self.days:
            hasData = False
            for j in self.dayObjs:
                if j.day == i:
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
        for i in self.days:
            hasData = False
            for j in self.dayObjs:
                if j.day == i:
                    hasData = True
                    prec.append(j.precipitation)
            if not hasData:
                prec.append(None)
        return prec

    def getSnowDepth(self):
        s = []
        for i in self.days:
            hasData = False
            for j in self.manualDayObjs:
                if j.day == i:
                    hasData = True
                    s.append(j.snowDepth)
            if not hasData:
                s.append(None)
        return s

    def generateTempDistribution(self):
        dist = []
        for l in range(len(Climate.TEMP_DISTRIBUTION_LIMITS)):
            sublist = []
            for i in self.days:
                hasData = False
                for j in self.dayObjs:
                    if j.day == i:
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
        for l in range(len(Climate.RH_DISTRIBUTION_LIMITS)):
            sublist = []
            for i in self.days:
                hasData = False
                for j in self.dayObjs:
                    if j.day == i:
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
        for l in range(len(Climate.WIND_DIRECTION_LIMITS)):
            sublist = []
            for i in self.days:
                hasData = False
                for j in self.dayObjs:
                    if j.day == i:
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
            'frostDays': Climate.get_nr_frost_days(self.tempMins),
            'coldDays': Climate.get_nr_cold_days(self.tempMins),
            'warmNights': Climate.get_nr_warm_nights(self.tempMins),
            'summerDays': Climate.get_nr_summer_days(self.tempMins),
            'warmDays': Climate.get_nr_warm_days(self.tempMins),
            'hotDays': Climate.get_nr_hot_days(self.tempMins)
        })

    def calculateDataAvailable(self):
        temp = Climate.number(self.tempMins) > 0 and Climate.number(self.tempMaxs) > 0
        tempDist = Climate.number2(self.generateTempDistribution()) > 0
        rhDist = Climate.number2(self.generateRhDistribution()) > 0
        prec = Climate.number(self.getPrecipitation()) > 0 and Climate.sum(self.getPrecipitation()) > 0
        windDist = Climate.number2(self.generateWindDistribution(), True) > 0
        sign = Climate.sum([self.monthObjs[0].significants.get(i) for i in self.monthObjs[0].significants]) > 0
        snowDepth = Climate.number(self.getSnowDepth()) > 0 and Climate.sum(self.getSnowDepth()) > 0
        return {
            "temp": temp,
            "tempDist": tempDist,
            "rhDist": rhDist,
            "prec": prec,
            "windDist": windDist,
            "sign": sign,
            "snowDepth": snowDepth,
        }

    def getComments(self):
        s = []
        for d in self.manualDayObjs:
            if d.comment and d.comment != "":
                s.append({
                    "day": d.day,
                    "comment": d.comment
                })
        return s

    def __init__(self, siteId, year, month, monthObjs, yearObj, dayObjs, manualDayObjs):
        self.siteId = siteId
        self.year = year
        self.month = month
        self.monthObjs = monthObjs
        self.yearObj = yearObj
        self.dayObjs = dayObjs
        self.manualDayObjs = manualDayObjs
        self.days = Month(year=self.year, month=self.month).days_of_month()
        self.tempMins, self.tempAvgs, self.tempMaxs = self.generateTemperatures()
        self.indices = self.calculateIndices()
        self.tempDist = json.dumps(self.generateTempDistribution())
        self.rhDist = json.dumps(self.generateRhDistribution())
        self.prec = json.dumps(self.getPrecipitation())
        self.precDist = Climate.get_precipitation_over_limits(self.getPrecipitation())
        self.windDist = json.dumps(self.generateWindDistribution())
        self.significants = json.dumps(monthObjs[0].significants)
        self.precipitation = Climate.sum(self.getPrecipitation())
        self.tmin = Climate.avg(self.tempMins)
        self.tmax = Climate.avg(self.tempMaxs)
        self.tavg = Climate.avg2(self.tempMins, self.tempMaxs)
        self.dataAvailable = self.calculateDataAvailable()
        self.tempMins = json.dumps(self.tempMins)
        self.tempAvgs = json.dumps(self.tempAvgs)
        self.tempMaxs = json.dumps(self.tempMaxs)
        self.snowDepths = json.dumps(self.getSnowDepth())
        self.snowDays = self.getNrOfSnowDays()
        self.comments = self.getComments()


class YearlyReport(Report):
    class Meta:
        managed = False

    def collectData(self, prop):
        dataset = []
        for i in self.months:
            hasData = False
            for j in self.monthObjs:
                if (j.month == i):
                    hasData = True
                    dataset.append(getattr(j, prop))
            if not hasData:
                dataset.append(None)
        return dataset

    def collectDailyData(self, prop):
        dataset = []
        for i in self.dayObjs:
            dataset.append(getattr(i, prop))
        return dataset

    def generateTempDistribution(self):
        dist = []
        for l in range(len(Climate.TEMP_DISTRIBUTION_LIMITS)):
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
        for l in range(len(Climate.RH_DISTRIBUTION_LIMITS)):
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
        for l in range(len(Climate.WIND_DIRECTION_LIMITS)):
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

    def calculateDataAvailable(self):
        temp = Climate.number(self.collectData('tempMin')) > 0 and Climate.number(self.collectData('tempMinAvg')) > 0
        tempDist = Climate.number2(self.generateTempDistribution(), strict=True) > 0
        rhDist = Climate.number2(self.generateRhDistribution(), strict=True) > 0
        prec = Climate.number(self.collectData('precipitation')) > 0 and Climate.sum(
            self.collectData('precipitation')) > 0
        windDist = Climate.number2(self.generateWindDistribution(), strict=True) > 0
        sign = False
        for m in self.monthObjs:
            if Climate.sum([self.monthObjs[0].significants.get(i) for i in self.monthObjs[0].significants]) > 0:
                sign = True
                break

        return {
            "temp": temp,
            "tempDist": tempDist,
            "rhDist": rhDist,
            "prec": prec,
            "windDist": windDist,
            "sign": sign
        }

    def __init__(self, siteId, year, monthObjs, yearObj, dayObjs, manualDayObjs):
        self.siteId = siteId
        self.year = year
        self.monthObjs = monthObjs
        self.yearObj = yearObj
        self.dayObjs = dayObjs
        self.manualDayObjs = manualDayObjs
        self.months = Year.months_of_year()
        self.temps = {
            'mins': json.dumps(self.collectData('tempMin')),
            'minAvgs': json.dumps(self.collectData('tempMinAvg')),
            'avgs': json.dumps(self.collectData('tempAvg')),
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
        self.precipitation = Climate.sum(self.collectData('precipitation'))
        self.precDist = Climate.get_precipitation_over_limits(self.collectDailyData('precipitation'))
        self.tmin = Climate.avg(self.collectData('tempMin'))
        self.tmax = Climate.avg(self.collectData('tempMax'))
        self.tavg = Climate.avg2(self.collectData('tempMin'), self.collectData('tempMax'))
        self.dataAvailable = self.calculateDataAvailable()
        self.snowDays = self.getNrOfSnowDays()


class RawObservation(models.Model):
    siteId = models.ForeignKey('climate.Site')
    createdDate = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    _weatherCode = models.CommaSeparatedIntegerField(max_length=200, choices=Weather.WEATHER_CODE, blank=True)
    windSpeed = models.IntegerField(choices=Weather.BEAUFORT_SCALE, default=0)

    # jelenség regisztrálása a statisztikákba
    def populateWeatherCode(self, arr):
        wc = ''
        for a in arr:
            wc = wc + a + ','
        self._weatherCode = wc
        self.save()

    @property
    def weatherCode(self):
        return self.convertToReadables(self._weatherCode[:-1].split(','))

    # return self._weatherCode.split(',')
    @weatherCode.setter
    def weatherCode(self, value):
        self._weatherCode = value

    def convertToReadables(self, codes):
        out = []
        for o in codes:
            out.append(self.convertToReadable(o))
        return out

    def convertToReadable(self, code):
        return Weather.get_weather_code_text(code)


class RawManualData(models.Model):
    """
    Manual data from a day
    """
    class Meta:
        unique_together = (('year', 'month', 'day', 'siteId'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField(default=-1)
    month = models.IntegerField(default=-1)
    day = models.IntegerField(default=-1)
    tMin = models.FloatField(blank=True, null=True)
    tMax = models.FloatField(blank=True, null=True)
    precAmount = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True)
    isSnow = models.BooleanField(default=False)
    snowDepth = models.FloatField(default=0.0)
    _weatherCode = models.CommaSeparatedIntegerField(max_length=200, choices=Weather.WEATHER_CODE, blank=True)

    def addWeatherCode(self, code):
        """
        Add weather observation code
        :param code:
        :return:
        """
        weatherCodes = self._weatherCode[:-1].split(',')
        if not code in weatherCodes:
            self._weatherCode = self._weatherCode + code + ','

    def populateWeatherCode(self, arr):
        wc = ''
        for a in arr:
            wc = wc + a + ','
        self._weatherCode = wc
        self.save()

    @property
    def weatherCode(self):
        if len(self._weatherCode[:-1]) > 0:
            return self._weatherCode[:-1].split(',')
        else:
            return []

    @weatherCode.setter
    def weatherCode(self, value):
        self._weatherCode = value


class DailyStat(models.Model):
    siteId = models.ForeignKey('climate.Site')
    date = models.DateField()


class MonthlyStat(models.Model):
    siteId = models.ForeignKey('climate.Site')
    date = models.DateField()
