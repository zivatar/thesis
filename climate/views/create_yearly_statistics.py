import logging

from climate.classes.Climate import Climate
from climate.models.RawData import RawData
from climate.models.RawManualData import RawManualData
from climate.models.YearlyStatistics import YearlyStatistics


def create_yearly_statistics(fromDate, toDate, siteId):
    logger = logging.getLogger(__name__)
    logger.error("create yearly stat from {} to {}".format(fromDate, toDate))
    fromDate = fromDate.replace(month=1, day=1, hour=0, minute=0, second=0)
    toDate = toDate.replace(month=12, day=31, hour=23, minute=59, second=59)
    f = fromDate
    while f < toDate:

        manual_data_set = RawManualData.objects.filter(siteId=siteId).filter(year=f.year)
        automatic_data_set = RawData.objects.filter(siteId=siteId).filter(createdDate__year=f.year)

        if len(manual_data_set) or len(automatic_data_set):
            d, created = YearlyStatistics.objects.update_or_create(siteId=siteId, year=f.year)

            significants = {}
            for day in manual_data_set:
                significants = Climate.count_significants(significants, day.weatherCode)

            d.significants = significants
            d.save()

        f = f.replace(year=f.year + 1)
    logger.error("create yearly stat finished")
    return 1
