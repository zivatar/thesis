import logging

import datetime
from threading import Timer

import pytz
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from climate.classes.Month import Month
from climate.models.RawData import RawData
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.views.create_daily_statistics import create_daily_statistics
from climate.views.create_monthly_statistics import create_monthly_statistics
from climate.views.create_yearly_statistics import create_yearly_statistics
from climate.views.handle_uploaded_data import handle_uploaded_data

logger = logging.getLogger(__name__)


def create_statistics(site, year=None, month=None, from_date=None, to_date=None, limitInMins=10):
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
            lastDate = datetime.datetime(year, month, Month(year=year, month=month).last_day(), 23, 59,
                                         tzinfo=pytz.timezone("Europe/Budapest"))
    else:
        if RawData.objects.filter(siteId=site).count() or RawManualData.objects.filter(siteId=site).count():
            hasData = True
            if RawData.objects.filter(siteId=site).count():
                firstDate1 = RawData.objects.filter(siteId=site).order_by('createdDate')[0].createdDate
                lastDate1 = RawData.objects.filter(siteId=site).order_by('-createdDate')[0].createdDate
            if RawManualData.objects.filter(siteId=site).count():
                fd2 = RawManualData.objects.filter(siteId=site).order_by('year').order_by('month').order_by('day')[0]
                ld2 = RawManualData.objects.filter(siteId=site).order_by('-year').order_by('-month').order_by('-day')[0]
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
        create_daily_statistics(firstDate, lastDate, site, limitInMins)
        create_monthly_statistics(firstDate, lastDate, site)
        create_yearly_statistics(firstDate, lastDate, site)


class UploadHandler(APIView):
    @staticmethod
    def _save_to_database(request, site):
        data = request.data.get('data', None)
        site = request.data.get('site', None)
        if data is None or site is None:
            raise Exception("try to save empty data or empty site")
        logger.error("try to save data from {} to {}".format(data[0], data[-1]))
        site_obj = get_object_or_404(Site, pk=site)
        inserted_lines = handle_uploaded_data(site=site_obj, data=data)
        UploadHandler._calculate_statistics(site=site_obj, data=data)

    @staticmethod
    def _calculate_statistics(site, data):
        from_date = datetime.datetime.fromtimestamp(data[0].get('date') / 1000,
                                                    tz=pytz.timezone("Europe/Budapest"))
        to_date = datetime.datetime.fromtimestamp(data[-1].get('date') / 1000,
                                                  tz=pytz.timezone("Europe/Budapest"))
        logger.error("calculate statistics for site {} from {} to {}".format(site, from_date, to_date))
        create_statistics(site=site, from_date=from_date, to_date=to_date)

    def post(self, request, *args, **kw):
        logger.error("POST request on UploadHandler")
        try:
            if request.data is None or 'site' not in request.data or 'data' not in request.data:
                raise Exception("Empty data or site")
            site = get_object_or_404(Site, pk=request.data.get('site', None))
            if request.user is None or not request.user.profile.canUpload or not site.isActive:
                raise Exception("Unauthorized")

            logger.error('POST request at UploadHandler for site {}'.format(site))
            t = Timer(0, lambda: UploadHandler._save_to_database(request, site))
            t.start()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=ex.strerror)
