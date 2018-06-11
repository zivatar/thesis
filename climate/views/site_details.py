from django.shortcuts import get_object_or_404, render

from climate.classes.Weather import Weather
from climate.models.Instrument import Instrument
from climate.models.MonthlyStatistics import MonthlyStatistics
from climate.models.RawObservation import RawObservation
from climate.models.Site import Site
from climate.models.YearlyStatistics import YearlyStatistics


def collect_monthly_report_data(yearly, monthly):
    """
    Create data structure for Site Details

    :param yearly: YearlyStatistics.objects
    :param monthly: MonthlyStatistics.objects
    :return: ``[{'year': y, 'months': [m, ...]}, ...]``
    """
    com = []
    for y in yearly:
        mo = []
        for m in monthly:
            if m.year == y.year:
                mo.append(m)
        com.append({'year': y, 'months': mo})
    return com


def site_details(request, pk):
    """
    Site details

    :param request: HTTP request
    :param pk: primary key of site
    :return: if public or own site of the user, renders ``climate/site_details.html``, else renders main page
    """
    print("site details")
    site = get_object_or_404(Site, pk=pk)
    if site.isPublic and site.owner.is_active or site.owner == request.user:
        observations = RawObservation.objects.filter(siteId=site).order_by('-createdDate')[:3]
        yearly = YearlyStatistics.objects.filter(siteId=site).order_by('year')
        monthly = MonthlyStatistics.objects.filter(siteId=site).order_by('month')
        ym = collect_monthly_report_data(yearly, monthly)
        instruments = Instrument.objects.filter(siteId=site).filter(isDeleted=False).order_by('title')
        return render(request, 'climate/site_details.html',
                      {'site': site, 'observations': observations, 'weather_code': Weather.WEATHER_CODE,
                       'ym': ym,
                       'instruments': instruments})
    else:
        return render(request, 'climate/main.html', {})
