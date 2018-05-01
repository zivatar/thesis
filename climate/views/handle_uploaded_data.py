import datetime

import pytz

from climate.classes.Number import Number
from climate.models.RawData import RawData


def handle_uploaded_data(site, data):
    start = datetime.datetime.fromtimestamp(data[0].get('date', None) / 1000, tz=pytz.timezone("Europe/Budapest"))
    end = datetime.datetime.fromtimestamp(data[-1].get('date', None) / 1000, tz=pytz.timezone("Europe/Budapest"))
    existing = RawData.objects.filter(createdDate__range=(start, end), siteId=site)
    existing_dates = existing.values_list('createdDate', flat=True)

    # for line in data:
    #     if datetime.datetime.fromtimestamp(line.get('date', None) / 1000,
    #                                        tz=pytz.timezone("Europe/Budapest")) not in existing_dates:
    #         logger.debug(datetime.datetime.fromtimestamp(line.get('date', None) / 1000,
    #                                                      tz=pytz.timezone("Europe/Budapest")))
    #         logger.debug(line)

    RawData.objects.bulk_create(
        RawData(siteId=site,
                createdDate=datetime.datetime.fromtimestamp(line.get('date', None) / 1000,
                                                            tz=pytz.timezone("Europe/Budapest")),
                dewpoint=Number.to_float(line.get('dewpoint', None)),
                precipitation=Number.to_float(line.get('precipitation', None)),
                humidity=Number.to_int(line.get('relativeHumidity', None)),
                pressure=Number.to_float(line.get('relativePressure', None)),
                humidityIn=Number.to_int(line.get('rhIndoor', None)),
                tempIn=Number.to_float(line.get('tempIndoor', None)),
                temperature=Number.to_float(line.get('temperature', None)),
                windChill=Number.to_float(line.get('windChill', None)),
                windSpeed=Number.to_float(line.get('windSpeed', None)),
                windDir=Number.to_float(line.get('windDirection', None)),
                gust=Number.to_float(line.get('windGustSpeed', None))
                )

        for line in data
        if datetime.datetime.fromtimestamp(line.get('date', None) / 1000,
                                           tz=pytz.timezone("Europe/Budapest")) not in existing_dates
    )
