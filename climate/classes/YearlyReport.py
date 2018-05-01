import simplejson as json

from climate.classes.Report import Report
from climate.classes.Climate import Climate
from climate.classes.Year import Year


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
            'winterDays': json.dumps(self.collectData('winterDays')),
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
        self.snowDays = self.get_nr_of_snow_days()
