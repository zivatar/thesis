import simplejson as json

from climate.classes.Report import Report
from climate.classes.Climate import Climate
from climate.classes.Month import Month


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
            'winterDays': Climate.get_nr_winter_days(self.tempMaxs),
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
        self.monthObj = Month(year=self.year, month=self.month)
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
