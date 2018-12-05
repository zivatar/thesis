import logging
from threading import Timer

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from climate.classes.Number import Number
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.views.UploadHandler import UploadHandler

logger = logging.getLogger(__name__)

class UploadClimateHandler(APIView):
    """
    Handler for manual climate data
    """

    @staticmethod
    def _process_data(site, year, month, data):
        """
        Saves RawManualData to DB, starts statistics calculation

        :param site: Site of data
        :param year: current year
        :param month: current month
        :param data: input data
        :return: None
        """
        logger.info("start processing manual data")
        UploadClimateHandler._saveToDb(site=site, year=year, month=month, data=data)
        UploadHandler.create_statistics(site=site, year=year, month=month)

    @staticmethod
    def _saveToDb(site, year, month, data):
        """
        Save data to DB

        :param site: Site object to save data
        :param year: current year
        :param month: current month
        :param data: input data
        :return: None
        """
        for i in range(len(data)):
            if data[i] is not None:
                d, created = RawManualData.objects.update_or_create(
                    siteId=site,
                    year=year,
                    month=month,
                    day=i + 1
                )
                if Number.is_number(data[i].get('Tmin', None)):
                    d.tMin = float(data[i].get('Tmin'))
                if Number.is_number(data[i].get('Tmax', None)):
                    d.tMax = float(data[i].get('Tmax'))
                if Number.is_number(data[i].get('prec', None)):
                    d.precAmount = float(data[i].get('prec'))
                if data[i].get('obs') is not None:
                    d.populate_weather_code(data[i].get('obs'))
                if data[i].get('comment') is not None:
                    d.comment = data[i].get('comment')
                if data[i].get('isSnow') is not None:
                    d.isSnow = data[i].get('isSnow')
                if data[i].get('snowDepth') is not None:
                    d.snowDepth = data[i].get('snowDepth')
                d.save()

    def post(self, request, *args, **kw):
        """
        HTTP POST request handler

        :param request: HTTP request
        :param args: arguments
        :param kw: keyword arguments
        :return: HTTP response
        """
        site = get_object_or_404(Site, pk=request.data.get('site'))
        dataset = request.data["data"]
        year = dataset.get('year')
        month = dataset.get('month')
        data = dataset.get('data')

        response = Response(None, status=status.HTTP_400_BAD_REQUEST)
        if request.user is not None:
            if request.data is not None and 'site' in request.data:
                site = get_object_or_404(Site, pk=request.data.get('site', None))
                if site.isActive and 'data' in request.data:
                    response = Response(None, status=status.HTTP_204_NO_CONTENT)
                    t = Timer(0, lambda: UploadClimateHandler._process_data(site=site,
                                                                            year=year,
                                                                            month=month,
                                                                            data=data))
                    t.start()
        return response
