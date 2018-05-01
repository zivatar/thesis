import decimal
import logging

import datetime

from django.db import transaction

from climate.classes.Climate import Climate
from climate.models.DailyStatistics import DailyStatistics
from climate.models.RawData import RawData
from climate.models.RawManualData import RawManualData


def create_daily_statistics(fromDate, toDate, siteId, limitInMins=3):
    logger = logging.getLogger(__name__)
    logger.error("create daily stat from {} to {}".format(fromDate, toDate))

    limit = datetime.timedelta(minutes=(limitInMins))
    fromDate = fromDate.replace(hour=0, minute=0, second=0)
    delta = toDate - fromDate

    existing = DailyStatistics.objects.filter(year__range=(fromDate.year, toDate.year), siteId=siteId).values()
    existing_dates = []
    logger.error(existing_dates)
    for i in existing:
        existing_dates.append(datetime.date(year=i.get('year'),
                                            month=i.get('month'),
                                            day=i.get('day')))
    daily_data = []

    for i in range(delta.days + 1):
        f = fromDate + datetime.timedelta(days=i)
        t = fromDate + datetime.timedelta(days=i + 1)
        rawDataSet = RawData.objects.filter(siteId=siteId, createdDate__year=f.year,
                                            createdDate__month=f.month, createdDate__day=f.day)
        manualDataSet = RawManualData.objects.filter(siteId=siteId, year=f.year, month=f.month, day=f.day)
        precipitation = None
        if rawDataSet.count() or manualDataSet.count():
            d = {'year': f.year, 'month': f.month, 'day': f.day, 'siteId': siteId}
            d['existing'] = datetime.date(year=f.year, month=f.month, day=f.day) in existing_dates
            daily_data.append(d)
        if rawDataSet.count():
            d['dataAvailable'] = rawDataSet.count()
            temps = []
            rhs = []
            winds = []
            last_timestamp = None
            for j in rawDataSet:
                current_timestamp = j.createdDate
                if not last_timestamp or (current_timestamp - last_timestamp) >= limit:
                    if j.temperature is not None:
                        temps.append(j.temperature)
                    if j.humidity is not None:
                        rhs.append(j.humidity)
                    if j.precipitation is not None:
                        if precipitation is None:
                            precipitation = decimal.Decimal(0.0)
                        else:
                            precipitation = precipitation + j.precipitation
                    if j.windDir is not None:
                        winds.append(j.windDir)
                    last_timestamp = current_timestamp
            tempDistribution = Climate.calculate_temperature_distribution(temps)
            d['tempDistribution'] = ''.join(str(e) + ',' for e in tempDistribution)[:-1]
            rhDistribution = Climate.calculate_rh_distribution(rhs)
            d['rhDistribution'] = ''.join(str(e) + ',' for e in rhDistribution)[:-1]
            windDistribution = Climate.calculate_wind_distribution(winds)
            d['windDistribution'] = ''.join(str(e) + ',' for e in windDistribution)[:-1]
            if len(temps) > 0:
                d['tempMin'] = min(temps)
                d['tempMax'] = max(temps)
                d['tempAvg'] = sum(temps) / len(temps)
            if precipitation is not None:
                d['precipitation'] = precipitation
        if manualDataSet.count():
            d['dataAvailable'] = d.get('dataAvailable', 0)
            if manualDataSet[0].tMin is not None:
                d['tempMin'] = manualDataSet[0].tMin
            if manualDataSet[0].tMax is not None:
                d['tempMax'] = manualDataSet[0].tMax
            if manualDataSet[0].precAmount is not None:
                d['precipitation'] = manualDataSet[0].precAmount

    logger.error("bulk create")
    DailyStatistics.objects.bulk_create(
        DailyStatistics(
            year=d.get('year'),
            month=d.get('month'),
            day=d.get('day'),
            siteId=d.get('siteId'),
            dataAvailable=d.get('dataAvailable'),
            tempMin=d.get('tempMin'),
            tempMax=d.get('tempMax'),
            tempAvg=d.get('tempAvg'),
            precipitation=d.get('precipitation'),
            tempDistribution=d.get('tempDistribution', ''),
            rhDistribution=d.get('rhDistribution', ''),
            windDistribution=d.get('windDistribution', '')
        )
        for d in daily_data
        if not d.get('existing')
    )

    logger.error("almost bulk update")
    with transaction.atomic():
        for d in daily_data:
            if d.get(existing):
                DailyStatistics.objects.filter(siteID=d.get('siteId'), year=d.get('year'),
                                               month=d.get('month'), day=d.get('day')).update(
                    dataAvailable=d.get('dataAvailable'),
                    tempMin=d.get('tempMin'),
                    tempMax=d.get('tempMax'),
                    tempAvg=d.get('tempAvg'),
                    precipitation=d.get('precipitation'),
                    tempDistribution=d.get('tempDistribution', ''),
                    rhDistribution=d.get('rhDistribution', ''),
                    windDistribution=d.get('windDistribution', '')
                )
    logger.error("daily stat finished")

    return 1
