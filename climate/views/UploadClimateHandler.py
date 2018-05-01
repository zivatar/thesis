from threading import Timer

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from climate.classes.Number import Number
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.views.UploadHandler import create_statistics


class UploadClimateHandler(APIView):

    def post(self, request, *args, **kw):
        site = get_object_or_404(Site, pk=request.data.get('site'))
        dataset = request.data["data"]
        year = dataset.get('year')
        month = dataset.get('month')
        data = dataset.get('data')

        def _saveToDb():
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
                        d.populateWeatherCode(data[i].get('obs'))
                    if data[i].get('comment') is not None:
                        d.comment = data[i].get('comment')
                    if data[i].get('isSnow') is not None:
                        d.isSnow = data[i].get('isSnow')
                    if data[i].get('snowDepth') is not None:
                        d.snowDepth = data[i].get('snowDepth')
                    d.save()

        def _calculateStatistics():
            create_statistics(site=site, year=year, month=month)

        if request.user != None:  # and request.user.can_upload:
            if request.data != None and 'site' in request.data:
                site = get_object_or_404(Site, pk=request.data.get('site', None))
                if site.isActive and 'data' in request.data:
                    response = Response(None, status=status.HTTP_204_NO_CONTENT)
                    t = Timer(0, _saveToDb)
                    t.start()
                    t = Timer(0, _calculateStatistics)
                    t.start()
        return response

