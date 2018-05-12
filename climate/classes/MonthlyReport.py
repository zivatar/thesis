import simplejson as json

from climate.classes.Report import Report
from climate.classes.Climate import Climate
from climate.classes.Month import Month


class MonthlyReport(Report):
    """
    | Monthly report
    | managed: False
    """

    class Meta:
        managed = False

    def collect_daily_temperature(self):
        """
        | Collect daily average, minimum and maximum temperature values

        :return: minimum temperature list, average temperature list, maximum temperature list
        """
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

    def collect_daily_precipitation(self):
        """
        | Collect daily precipitation values

        :return: precipitation list
        """
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

    def collect_snow_depth(self):
        """
        | Collect every morning snow depth data

        :return: snow depth list
        """
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

    def generate_temp_distribution(self):
        """
        | Generate temperature distribution

        :return: temperature distribution list
        """
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

    def generate_rh_distribution(self):
        """
        | Generate relative humidity distribution

        :return: relative humidity distribution list
        """
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

    def generate_wind_distribution(self):
        """
        | Generate wind direction distribution

        :return: wind direction distribution list
        """
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

    def calculate_climate_index_days(self):
        """
        | Calculate climate index days

        :return: {'frostDays': fd, 'winterDays': wd, 'coldDays': cd, 'warmNights': wn, 'summerDays': sd, 'warmDays': wwd, 'hotDays': hd}
        """
        return ({
            'frostDays': Climate.get_nr_frost_days(self.tempMins),
            'winterDays': Climate.get_nr_winter_days(self.tempMaxs),
            'coldDays': Climate.get_nr_cold_days(self.tempMins),
            'warmNights': Climate.get_nr_warm_nights(self.tempMins),
            'summerDays': Climate.get_nr_summer_days(self.tempMins),
            'warmDays': Climate.get_nr_warm_days(self.tempMins),
            'hotDays': Climate.get_nr_hot_days(self.tempMins)
        })

    def calculate_number_of_available_data(self):
        """
        | Calculate number of available data

        :return: {"temp": temp, "tempDist": tempDist, "rhDist": rhDist, "prec": prec, "windDist": windDist, "sign": sign, "snowDepth": snowDepth}
        """
        temp = Climate.number(self.tempMins) > 0 and Climate.number(self.tempMaxs) > 0
        tempDist = Climate.number2(self.generate_temp_distribution()) > 0
        rhDist = Climate.number2(self.generate_rh_distribution()) > 0
        prec = Climate.number(self.collect_daily_precipitation()) > 0 and Climate.sum(
            self.collect_daily_precipitation()) > 0
        windDist = Climate.number2(self.generate_wind_distribution(), True) > 0
        sign = Climate.sum([self.monthObjs[0].significants.get(i) for i in self.monthObjs[0].significants]) > 0
        snowDepth = Climate.number(self.collect_snow_depth()) > 0 and Climate.sum(self.collect_snow_depth()) > 0
        return {
            "temp": temp,
            "tempDist": tempDist,
            "rhDist": rhDist,
            "prec": prec,
            "windDist": windDist,
            "sign": sign,
            "snowDepth": snowDepth,
        }

    def get_comments(self):
        """
        Get comments of manual raw data

        :return: list of { "day": d, "comment": c }
        """
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
        self.days = Month(year=self.year, month=self.month).get_days_of_month()
        self.tempMins, self.tempAvgs, self.tempMaxs = self.collect_daily_temperature()
        self.indices = self.calculate_climate_index_days()
        self.tempDist = json.dumps(self.generate_temp_distribution())
        self.rhDist = json.dumps(self.generate_rh_distribution())
        self.prec = json.dumps(self.collect_daily_precipitation())
        self.precDist = Climate.get_precipitation_over_limits(self.collect_daily_precipitation())
        self.windDist = json.dumps(self.generate_wind_distribution())
        self.significants = json.dumps(monthObjs[0].significants)
        self.precipitation = Climate.sum(self.collect_daily_precipitation())
        self.tmin = Climate.avg(self.tempMins)
        self.tmax = Climate.avg(self.tempMaxs)
        self.tavg = Climate.avg2(self.tempMins, self.tempMaxs)
        self.dataAvailable = self.calculate_number_of_available_data()
        self.tempMins = json.dumps(self.tempMins)
        self.tempAvgs = json.dumps(self.tempAvgs)
        self.tempMaxs = json.dumps(self.tempMaxs)
        self.snowDepths = json.dumps(self.collect_snow_depth())
        self.snowDays = self.get_nr_of_snow_days()
        self.comments = self.get_comments()
