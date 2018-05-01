import decimal
import logging

from climate.classes.Climate import Climate
from climate.models.DailyStatistics import DailyStatistics
from climate.models.MonthlyStatistics import MonthlyStatistics
from climate.models.RawData import RawData
from climate.models.RawManualData import RawManualData


def create_monthly_statistics(fromDate, toDate, siteId):
    logger = logging.getLogger(__name__)
    logger.error("create monthly stat from {} to {}".format(fromDate, toDate))
    fromDate = fromDate.replace(hour=0, minute=0, second=0, day=1)
    if (toDate.month < 12):
        toDate = toDate.replace(month=toDate.month + 1, day=1, hour=0, minute=0, second=0)
    else:
        toDate = toDate.replace(year=toDate.year + 1, month=1, day=1, hour=0, minute=0, second=0)
    f = fromDate
    while f < toDate:
        rawDataSet = DailyStatistics.objects.filter(year=f.year, month=f.month).filter(siteId=siteId)
        logger.error("dailystat number: {}".format(rawDataSet.count()))
        if rawDataSet.count():
            d, created = MonthlyStatistics.objects.update_or_create(siteId=siteId, month=f.month, year=f.year)
            d.dataAvailable = rawDataSet.count()
            tempmins = []
            tempmaxs = []
            tempavgs = []
            precipitation = decimal.Decimal(0.0)
            for j in rawDataSet:
                if j.tempMin is not None:
                    tempmins.append(j.tempMin)
                if j.tempMax is not None:
                    tempmaxs.append(j.tempMax)
                if j.tempAvg is not None:
                    tempavgs.append(j.tempAvg)
                if j.precipitation is not None:
                    precipitation = precipitation + j.precipitation
            d.dataAvailable = rawDataSet.count()
            if len(tempmins) > 0:
                d.tempMin = min(tempmins)
                d.tempMinAvg = sum(tempmins) / len(tempmins)
            if len(tempmaxs) > 0:
                d.tempMax = max(tempmaxs)
                d.tempMaxAvg = sum(tempmaxs) / len(tempmaxs)
            if len(tempavgs) > 0:
                d.tempAvg = sum(tempavgs) / len(tempavgs)
            rawDataSet = RawData.objects.filter(createdDate__year=f.year,
                                                createdDate__month=f.month).filter(siteId=siteId)
            temps = []
            rhs = []
            winds = []
            for j in rawDataSet:
                if j.temperature is not None:
                    temps.append(j.temperature)
                if j.humidity is not None:
                    rhs.append(j.humidity)
                if j.windDir is not None:
                    winds.append(j.windDir)
            tempDistribution = Climate.calculate_temperature_distribution(temps)
            d.tempDistribution = ''.join(str(e) + ',' for e in tempDistribution)[:-1]
            rhDistribution = Climate.calculate_rh_distribution(rhs)
            d.rhDistribution = ''.join(str(e) + ',' for e in rhDistribution)[:-1]
            windDistribution = Climate.calculate_wind_distribution(winds)
            d.windDistribution = ''.join(str(e) + ',' for e in windDistribution)[:-1]
            d.precipitation = precipitation
            d.summerDays = Climate.get_nr_summer_days(tempmaxs)
            d.frostDays = Climate.get_nr_frost_days(tempmins)
            d.winterDays = Climate.get_nr_winter_days(tempmaxs)
            d.coldDays = Climate.get_nr_cold_days(tempmins)
            d.warmNights = Climate.get_nr_warm_nights(tempmins)
            d.warmDays = Climate.get_nr_warm_days(tempmaxs)
            d.hotDays = Climate.get_nr_hot_days(tempmaxs)

            manualDataSet = RawManualData.objects.filter(siteId=siteId).filter(year=f.year).filter(month=f.month)
            significants = {}
            for day in manualDataSet:
                significants = Climate.count_significants(significants, day.weatherCode)
            d.significants = significants
            d.save()

        if (f.month == 12):
            f = f.replace(year=f.year + 1, month=1)
        else:
            f = f.replace(month=f.month + 1)
    return 1

