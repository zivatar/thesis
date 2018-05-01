from django.shortcuts import get_object_or_404, render

from climate.classes.Climate import Climate
from climate.classes.MonthlyReport import MonthlyReport
from climate.classes.Weather import Weather
from climate.models.DailyStatistics import DailyStatistics
from climate.models.MonthlyStatistics import MonthlyStatistics
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.models.YearlyStatistics import YearlyStatistics


def monthly_report(request, site, year, month):
    """
    Monthly view
    :param request: HTTP request
    :param site:
    :param year:
    :param month:
    :return: html page
    """
    siteObj = get_object_or_404(Site, pk=site)
    yearly = YearlyStatistics.objects.filter(siteId=siteObj).filter(year=year)
    monthly = MonthlyStatistics.objects.filter(siteId=siteObj).filter(year=year).filter(month=month)
    daily = DailyStatistics.objects.filter(siteId=siteObj).filter(year=year).filter(month=month)
    dailyManual = RawManualData.objects.filter(siteId=siteObj).filter(year=year).filter(month=month)

    if siteObj and yearly and monthly and daily and (siteObj.isPublic and
                                                     siteObj.owner.is_active or siteObj.owner == request.user):
        climate = {'temp': Climate().TEMP_DISTRIBUTION_LIMITS, 'wind': Climate().WIND_DIRECTION_LIMITS,
                   'rh': Climate().RH_DISTRIBUTION_LIMITS}
        datasetNum = []
        a = MonthlyReport(site, year, month, monthly, yearly, daily, dailyManual)

        significants = {}
        for code in Weather.WEATHER_CODE:
            key = code[1]
            value = monthly[0].significants.get(code[0], 0)
            significants[key] = value

        return render(request, 'climate/monthly_view.html', {'site': siteObj, 'num': datasetNum, 'year': yearly,
                                                             'month': month, 'report': a, 'climate': climate,
                                                             'significants': significants})
    else:
        return render(request, 'climate/main.html', {})
