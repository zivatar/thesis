import simplejson as json

from climate.classes.Report import Report
from climate.classes.Climate import Climate
from climate.classes.Year import Year


class YearlyReport(Report):
    """
    | Yearly report
    | managed: False
    """

    class Meta:
        managed = False

    def collect_monthly_data(self, prop):
        """
        | Collect monthly data of year

        :param prop: 'tempMin', 'tempMax', 'precipitation', 'summerDays', ...
        :return: list of collected data
        """
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

    def collect_daily_data(self, prop):
        """
        | Collect daily data of year

        :param prop: 'precipitation'
        :return: list of collected data
        """
        dataset = []
        for i in self.dayObjs:
            dataset.append(getattr(i, prop))
        return dataset

    def generate_temperature_distribution(self):
        """
        | Generate temperature distribution

        :return: distribution list
        """
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

    def generate_rh_distribution(self):
        """
        | Generate relative humidity distribution

        :return: distribution list
        """
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

    def generate_wind_distribution(self):
        """
        | Generate wind distribution

        :return: distribution list
        """
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

    def calculate_number_of_available_data(self):
        """
        | Calculate number of available data for every months

        :return: {"temp": temp, "tempDist": tempDist, "rhDist": rhDist, "prec": prec, "windDist": windDist, "sign": sign }
        """
        temp = Climate.number(self.collect_monthly_data('tempMin')) > 0 and Climate.number(self.collect_monthly_data('tempMinAvg')) > 0
        tempDist = Climate.number2(self.generate_temperature_distribution(), strict=True) > 0
        rhDist = Climate.number2(self.generate_rh_distribution(), strict=True) > 0
        prec = Climate.number(self.collect_monthly_data('precipitation')) > 0 and Climate.sum(
            self.collect_monthly_data('precipitation')) > 0
        windDist = Climate.number2(self.generate_wind_distribution(), strict=True) > 0
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
        self.months = Year.get_months_of_year()
        self.temps = {
            'mins': json.dumps(self.collect_monthly_data('tempMin')),
            'minAvgs': json.dumps(self.collect_monthly_data('tempMinAvg')),
            'avgs': json.dumps(self.collect_monthly_data('tempAvg')),
            'maxAvgs': json.dumps(self.collect_monthly_data('tempMaxAvg')),
            'maxs': json.dumps(self.collect_monthly_data('tempMax'))
        }
        self.tempIndices = {
            'summerDays': json.dumps(self.collect_monthly_data('summerDays')),
            'frostDays': json.dumps(self.collect_monthly_data('frostDays')),
            'winterDays': json.dumps(self.collect_monthly_data('winterDays')),
            'coldDays': json.dumps(self.collect_monthly_data('coldDays')),
            'warmNights': json.dumps(self.collect_monthly_data('warmNights')),
            'warmDays': json.dumps(self.collect_monthly_data('warmDays')),
            'hotDays': json.dumps(self.collect_monthly_data('hotDays'))
        }
        self.prec = json.dumps(self.collect_monthly_data('precipitation'))
        self.tempDist = json.dumps(self.generate_temperature_distribution())
        self.rhDist = json.dumps(self.generate_rh_distribution())
        self.windDist = json.dumps(self.generate_wind_distribution())
        self.precipitation = Climate.sum(self.collect_monthly_data('precipitation'))
        self.precDist = Climate.get_precipitation_over_limits(self.collect_daily_data('precipitation'))
        self.tmin = Climate.avg(self.collect_monthly_data('tempMin'))
        self.tmax = Climate.avg(self.collect_monthly_data('tempMax'))
        self.tavg = Climate.avg2(self.collect_monthly_data('tempMin'), self.collect_monthly_data('tempMax'))
        self.dataAvailable = self.calculate_number_of_available_data()
        self.snowDays = self.get_nr_of_snow_days()
