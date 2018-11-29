import decimal
import logging

import datetime
from threading import Timer

import pytz
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from climate.classes.BadRequestException import BadRequestException
from climate.classes.Climate import Climate
from climate.classes.Month import Month
from climate.classes.Number import Number
from climate.models.DailyStatistics import DailyStatistics
from climate.models.MonthlyStatistics import MonthlyStatistics
from climate.models.UnprocessedData import UnprocessedData
from climate.models.RawData import RawData
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.models.YearlyStatistics import YearlyStatistics

logger = logging.getLogger(__name__)


class UploadHandler(APIView):
    """
    Handler for automatic data
    """

    INTERVAL = 10
    """Frequency of checking if statistics calculation needs to be started (seconds)"""

    EXPIRATION_TIME_IN_SECONDS = 60
    """Timeout to ensure all data arrives before we calculate statistics (seconds)"""

    is_interval_running = False

    @staticmethod
    def handle_uploaded_data(site, data):
        """
        Insert raw data into DB

        :param site: primary key for site
        :param data: data part of the HTTP request
        :return: number of new data
        """
        start = datetime.datetime.fromtimestamp(data[0].get('date', None) / 1000, tz=pytz.timezone("Europe/Budapest"))
        end = datetime.datetime.fromtimestamp(data[-1].get('date', None) / 1000, tz=pytz.timezone("Europe/Budapest"))
        existing = RawData.objects.filter(createdDate__range=(start, end), siteId=site)
        existing_dates = existing.values_list('createdDate', flat=True)

        bulk = RawData.objects.bulk_create(
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
        return len(bulk)

    @staticmethod
    def create_yearly_statistics(fromDate, toDate, siteId):
        """
        Create yearly stat

        :param fromDate: start date of the calculation
        :param toDate: end date of the calculation
        :param siteId: site
        :return: None
        """
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

    @staticmethod
    def create_monthly_statistics(fromDate, toDate, siteId):
        """
        | Create monthly stat

        :param fromDate: start date of calculation
        :param toDate: end date of the calculation
        :param siteId: site
        :return: None
        """
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

    @staticmethod
    def create_daily_statistics(fromDate, toDate, siteId, limitInMins=3):
        """
        | Create daily stat

        :param fromDate: start date of calculation
        :param toDate: end date of calculation
        :param siteId: site
        :param limitInMins: limit before calculation
        :return: None
        """
        logger = logging.getLogger(__name__)
        logger.error("create daily stat from {} to {}".format(fromDate, toDate))

        limit = datetime.timedelta(minutes=(limitInMins))
        fromDate = fromDate.replace(hour=0, minute=0, second=0)
        delta = toDate - fromDate

        existing = DailyStatistics.objects.filter(year__range=(fromDate.year, toDate.year), siteId=siteId).values()
        existing_dates = []
        logger.error("existing:")
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
        for d in daily_data:
            logger.error(d)
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

    @staticmethod
    def create_statistics(site, year=None, month=None, from_date=None, to_date=None, limitInMins=5):
        """
        Calculate monthly and yearly statistics between two limits

        :param site: primary key for site
        :param year: year to calculate (if only one month is needed)
        :param month: month to calculate (if only one month is needed)
        :param from_date: start date of calculation (if more months are needed)
        :type from_date: datetime
        :param to_date: end date of calculation (if more months are needed)
        :type to_date: datetime
        :param limitInMins: minimum gaps between data lines -- to handle data recording too often (minutes)
        :return: None
        """
        hasData = False
        if from_date is not None and to_date is not None:
            firstDate = from_date
            lastDate = to_date
            hasData = True
        elif year is not None and month is not None:
            if RawData.objects.filter(siteId=site,
                                      createdDate__year=year,
                                      createdDate__month=month).count() > 0 or \
                    RawManualData.objects.filter(siteId=site, year=year, month=month).count() > 0:
                hasData = True
                firstDate = datetime.datetime(year, month, 1, 0, 0, tzinfo=pytz.timezone("Europe/Budapest"))
                lastDate = datetime.datetime(year, month, Month(year=year, month=month).get_last_day(), 23, 59,
                                             tzinfo=pytz.timezone("Europe/Budapest"))
        else:
            if RawData.objects.filter(siteId=site).count() or RawManualData.objects.filter(siteId=site).count():
                hasData = True
                if RawData.objects.filter(siteId=site).count():
                    firstDate1 = RawData.objects.filter(siteId=site).order_by('createdDate')[0].createdDate
                    lastDate1 = RawData.objects.filter(siteId=site).order_by('-createdDate')[0].createdDate
                if RawManualData.objects.filter(siteId=site).count():
                    fd2 = RawManualData.objects.filter(siteId=site).order_by('year').order_by('month').order_by('day')[
                        0]
                    ld2 = \
                        RawManualData.objects.filter(siteId=site).order_by('-year').order_by('-month').order_by('-day')[
                            0]
                    firstDate2 = datetime.datetime(fd2.year, fd2.month, fd2.day, 0, 0,
                                                   tzinfo=pytz.timezone("Europe/Budapest"))
                    lastDate2 = datetime.datetime(ld2.year, ld2.month, ld2.day, 23, 59,
                                                  tzinfo=pytz.timezone("Europe/Budapest"))
                if RawData.objects.filter(siteId=site).count() and RawManualData.objects.filter(siteId=site).count():
                    firstDate = min(firstDate1, firstDate2)
                    lastDate = max(lastDate1, lastDate2)
                elif RawData.objects.filter(siteId=site).count():
                    firstDate = firstDate1
                    lastDate = lastDate1
                elif RawManualData.objects.filter(siteId=site).count():
                    firstDate = firstDate2
                    lastDate = lastDate2
        if hasData:
            UploadHandler.create_daily_statistics(firstDate, lastDate, site, limitInMins)
            UploadHandler.create_monthly_statistics(firstDate, lastDate, site)
            UploadHandler.create_yearly_statistics(firstDate, lastDate, site)

    @staticmethod
    def _save_to_database(request):
        """
        Save to DB and start calculation

        :param request: HTTP request
        :return: None
        """
        data = request.data.get('data', None)
        site = request.data.get('site', None)
        if data is None or site is None:
            raise Exception("try to save empty data or empty site")
        logger.error("try to save data from {} to {}".format(data[0], data[-1]))
        site_obj = get_object_or_404(Site, pk=site)
        number_of_inserted_lines = UploadHandler.handle_uploaded_data(site=site_obj, data=data)
        if number_of_inserted_lines:
            UploadHandler._calculate_statistics(site=site_obj, data=data)

    @staticmethod
    def _check_if_statistics_calculation_is_needed():
        """
        Check if all temporary data of a site are expired

        :return: None
        """
        expiration_date = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(
            seconds=UploadHandler.EXPIRATION_TIME_IN_SECONDS)
        not_expired_data = UnprocessedData.objects.filter(uploaded_at__gte=expiration_date)
        sites_of_not_expired_data = not_expired_data.values_list('site_id', flat=True).distinct()
        all_sites = UnprocessedData.objects.filter(uploaded_at__lte=expiration_date).values_list('site_id',
                                                                                                 flat=True).distinct()
        for s in all_sites:
            if s not in sites_of_not_expired_data:
                from_date = UnprocessedData.objects.filter(site_id_id=s).order_by('from_date')[0].from_date
                to_date = UnprocessedData.objects.filter(site_id_id=s).order_by('-to_date')[0].to_date
                print("should create stats for {} from {} to {}".format(s, from_date, to_date))
                site_obj = get_object_or_404(Site, pk=s)
                UploadHandler.create_statistics(site=site_obj, from_date=from_date, to_date=to_date)
                UnprocessedData.objects.filter(site_id_id=s).delete()

        if len(sites_of_not_expired_data):
            Timer(UploadHandler.INTERVAL, UploadHandler._check_if_statistics_calculation_is_needed).start()
        else:
            UploadHandler.is_interval_running = False

    @staticmethod
    def _create_temporary_data(from_date, to_date, site):
        """
        Create temporary data

        :param from_date: start date
        :param to_date: end date
        :param site: primary key for site
        :return: None
        """
        UnprocessedData.objects.create(site_id=site, from_date=from_date, to_date=to_date,
                                       uploaded_at=datetime.datetime.now(tz=datetime.timezone.utc))
        if not UploadHandler.is_interval_running:
            Timer(UploadHandler.INTERVAL, UploadHandler._check_if_statistics_calculation_is_needed).start()
            UploadHandler.is_interval_running = True

    @staticmethod
    def _calculate_statistics(site, data):
        """
        Start statistics generation from automatic data

        :param site: primary key for site
        :param data: data
        :return: None
        """
        from_date = datetime.datetime.fromtimestamp(data[0].get('date') / 1000,
                                                    tz=pytz.timezone("Europe/Budapest"))
        to_date = datetime.datetime.fromtimestamp(data[-1].get('date') / 1000,
                                                  tz=pytz.timezone("Europe/Budapest"))
        logger.debug("calculate statistics for site {} from {} to {}".format(site, from_date, to_date))
        UploadHandler._create_temporary_data(site=site, from_date=from_date, to_date=to_date)
        # create_statistics(site=site, from_date=from_date, to_date=to_date)

    def post(self, request, *args, **kw):
        """
        HTTP POST request handler

        :param request: HTTP request
        :param args: arguments
        :param kw: keyword arguments
        :return: HTTP response
        """
        logger.debug("POST request on UploadHandler")
        try:
            if request.data is None or 'site' not in request.data or 'data' not in request.data:
                raise BadRequestException("Empty data or site")
            site = get_object_or_404(Site, pk=request.data.get('site', None))
            logger.error('POST request at UploadHandler for site {}'.format(site))
            if request.user is None or not request.user.profile.canUpload or not site.isActive:
                raise BadRequestException("Unauthorized")
            Timer(0, lambda: UploadHandler._save_to_database(request)).start()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except BadRequestException as ex:
            logger.debug(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=ex.strerror)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=ex.strerror)
