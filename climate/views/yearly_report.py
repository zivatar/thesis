from django.shortcuts import get_object_or_404, render

from climate.classes.Climate import Climate
from climate.classes.Weather import Weather
from climate.classes.YearlyReport import YearlyReport
from climate.constant import monthList
from climate.models.DailyStatistics import DailyStatistics
from climate.models.MonthlyStatistics import MonthlyStatistics
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.models.YearlyStatistics import YearlyStatistics


def yearly_report(request, pk, year):
    """
    Yearly report of a site

    :param request: HTTP request
    :param pk: primary key of a site
    :param year: year
    :return: renders ``climate/yearly_view.html``
    """
    site = get_object_or_404(Site, pk=pk)
    yearlyList = YearlyStatistics.objects.filter(siteId=site).filter(year=year)
    if len(yearlyList) > 0:
        yearly = yearlyList[0]
    monthly = MonthlyStatistics.objects.filter(siteId=site).filter(year=year).order_by('month')
    daily = DailyStatistics.objects.filter(siteId=site).filter(year=year).order_by('month')
    dailyManual = RawManualData.objects.filter(siteId=site).filter(year=year)

    if site and yearlyList and monthly and (site.isPublic and site.owner.is_active or site.owner == request.user):
        climate = {'temp': Climate().TEMP_DISTRIBUTION_LIMITS, 'wind': Climate().WIND_DIRECTION_LIMITS,
                   'rh': Climate().RH_DISTRIBUTION_LIMITS}
        datasetNum = []
        for i in range(12):
            added = False
            for j in monthly:
                if j.month == i + 1:
                    datasetNum.append({'id': i + 1, 'available': j.dataAvailable})
                    added = True
            if not added:
                datasetNum.append({'id': i + 1, 'available': 0})
        a = YearlyReport(site, year, monthly, yearly, daily, dailyManual)

        significants = {}
        for code in Weather.WEATHER_CODE:
            key = code[1]
            value = yearly.significants.get(code[0], 0)
            significants[key] = value

        return render(request, 'climate/yearly_view.html', {'site': site, 'year': yearly,
                                                            'monthNames': monthList, 'num': datasetNum,
                                                            'report': a,
                                                            'climate': climate, 'significants': significants})
    else:
        return render(request, 'climate/main.html', {})
