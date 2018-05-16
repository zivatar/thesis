import simplejson as json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from climate.classes.Month import Month
from climate.classes.Weather import Weather
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.views.main import main


@login_required
def climate(request, pk, year=None, month=None):
    """
    | Climate diary of a site for a specific month
    | It contains earlier saved climate observations
    | And a form to record new ones
    | Login required

    :param request: HTTP request
    :param pk: primary key of site
    :param year: year
    :param month: month
    :return: renders ``climate/climate.html`` with appropriate data
    """
    site = get_object_or_404(Site, pk=pk)
    if year and month:
        real_month = Month()
        this_month = Month(year=year, month=month)
        if this_month.year > real_month.year or this_month.month > real_month.month:
            return redirect(main)
        elif this_month.year == real_month.year and this_month.month == real_month.month:
            this_month = real_month
    else:
        this_month = Month()
    actualDataJson = []
    for i in this_month.get_days_of_month_till_today():
        actualData = RawManualData.objects.filter(year=this_month.year, month=this_month.month, siteId=pk, day=i)
        if len(actualData) > 0:
            actualDataJson.append({
                "Tmin": actualData[0].tMin,
                "Tmax": actualData[0].tMax,
                "prec": actualData[0].precAmount,
                "obs": actualData[0].weatherCode,
                "isSnow": actualData[0].isSnow,
                "snowDepth": actualData[0].snowDepth,
                "comment": actualData[0].comment
            })
        else:
            actualDataJson.append(None)
    return render(request, 'climate/climate.html',
                  {'site': site, 'actualData': json.dumps(actualDataJson), 'month': this_month,
                   'weatherCodes': Weather.WEATHER_CODE})
