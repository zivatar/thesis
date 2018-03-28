import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .classes.weather import Weather
from .classes.climate import Climate
from .models import Site, Instrument
from .models import RawObservation, RawManualData, Month, RawData
from .models import DailyStatistics, MonthlyStatistics, YearlyStatistics
from .models import MonthlyReport, YearlyReport
from .forms import SiteForm, ObservationForm, DiaryForm, RegistrationForm, UserForm, InstrumentForm
from django.utils import timezone
from re import sub
from datetime import datetime
import dateutil.parser as dtparser
import calendar
import datetime
import decimal
import time
import pytz
import simplejson as json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from threading import Timer

from .utils import gravatar as gr
from django.template.defaulttags import register

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

WAIT_BEFORE_CALCULATE_STATISTICS = 1 # sec
monthList = ['J', 'F', 'M', 'Á', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def is_admin(user):
    if user:
        return user.is_superuser
    return False


def can_upload(user):
    if user:
        return user.profile.canUpload
    return False


def site_list(request):
    sites = Site.objects.filter(isPublic=True).filter().order_by('title')
    return render(request, 'climate/site_list.html', {'sites': sites})


@login_required
def own_site_list(request):
    sites = Site.objects.filter(owner=request.user).filter(isDeleted=False).order_by('title')
    return render(request, 'climate/site_list.html', {'sites': sites})


@login_required
def own_instrument_list(request):
    instruments = Instrument.objects.filter(siteId__owner=request.user).filter(isDeleted=False).order_by('title')
    return render(request, 'climate/instrument_list.html', {'instruments': instruments})


@login_required
def site_edit(request, pk):
    site = get_object_or_404(Site, pk=pk)
    if (site.owner == request.user):
        if request.method == "POST":
            form = SiteForm(request.POST, request.FILES, instance=site)
            if form.is_valid():
                site = form.save(commit=False)
                site.save()
                return redirect(site_edit, pk=site.pk)
        else:
            form = SiteForm()
            sites = Site.objects.filter(owner=request.user)
        return render(request, 'climate/site_edit.html',
                      {'sites': sites, 'wide_area': Site.WIDE_AREA, 'narrow_area': Site.NARROW_AREA, 'form': form,
                       'site': site})
    else:
        return render(request, 'climate/main.html', {})


@login_required
def new_instrument(request):
    sites = Site.objects.filter(owner=request.user)
    if request.method == "POST":
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
            return redirect(own_instrument_list)
    else:
        form = InstrumentForm()
    return render(request, 'climate/new_instrument.html', {'sites': sites, 'form': form})


@login_required
def my_user(request):
    logger.debug("views.my_user")
    print(1)
    logger.error(2)
    user = request.user
    gravatar = gr.gravatar_url(user.email)
    return render(request, 'climate/my_user.html', {'user': user, 'gravatar': gravatar})


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def edit_users(request):
    myUser = request.user
    users = User.objects.all().select_related('profile')
    return render(request, 'climate/edit_users.html', {'user': myUser, 'users': users})


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def edit_user(request, user):
    userObj = get_object_or_404(User, pk=user)
    gravatar = gr.gravatar_url(userObj.email)
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            userObj.is_active = cd.get('isActive')
            userObj.is_superuser = cd.get('isAdmin')
            userObj.profile.canUpload = cd.get('canUpload')
            userObj.save()
            return redirect(edit_users)
    else:
        form = UserForm(initial={"isAdmin": is_admin(userObj), "isActive": userObj.is_active,
                                 "canUpload": userObj.profile.canUpload})
    return render(request, 'climate/edit_user.html', {'editUser': userObj, 'form': form, 'gravatar': gravatar})


def guide(request):
    return render(request, 'climate/guide.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(main)
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def new_site(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.owner = request.user
            site.save()
            sites = Site.objects.filter(owner=request.user)
            return redirect(site_list)
    else:
        form = SiteForm()
        sites = Site.objects.filter(owner=request.user)
    return render(request, 'climate/new_site.html',
                  {'sites': sites, 'wide_area': Site.WIDE_AREA, 'narrow_area': Site.NARROW_AREA, 'form': form})


@login_required
def new_observation(request):
    sites = Site.objects.filter(owner=request.user)
    if request.method == "POST":
        form = ObservationForm(request.POST)
        if form.is_valid():
            obs = form.save()
            weatherCodes = form.cleaned_data.get('weatherCode')
            obs.populateWeatherCode(weatherCodes)
            dailyData, created = RawManualData.objects.update_or_create(year=obs.createdDate.year,
                                                                        month=obs.createdDate.month, siteId=obs.siteId,
                                                                        day=obs.createdDate.day)
            for code in weatherCodes:
                dailyData.addWeatherCode(code)
            dailyData.save()
            create_statistics(obs.siteId, obs.createdDate.year, obs.createdDate.month)
            return redirect(main)
    else:
        form = ObservationForm()
    return render(request, 'climate/new_observation.html',
                  {'sites': sites, 'form': form, 'wind_speed': Weather.BEAUFORT_SCALE,
                   'weather_code': Weather.WEATHER_CODE})


def main(request):
    return render(request, 'climate/main.html', {})


def createYearlyMonthly(yearly, monthly):
    com = []
    for y in yearly:
        mo = []
        for m in monthly:
            if (m.year == y.year):
                mo.append(m)
        com.append({'year': y, 'months': mo})
    return com


def site_details(request, pk):
    site = get_object_or_404(Site, pk=pk)
    if site.isPublic and site.owner.is_active or site.owner == request.user:
        observations = RawObservation.objects.filter(siteId=site).order_by('-createdDate')[:3]
        yearly = YearlyStatistics.objects.filter(siteId=site).order_by('year')
        monthly = MonthlyStatistics.objects.filter(siteId=site).order_by('month')
        ym = createYearlyMonthly(yearly, monthly)
        instruments = Instrument.objects.filter(siteId=site).filter(isDeleted=False).order_by('title')
        return render(request, 'climate/site_details.html',
                      {'site': site, 'observations': observations, 'weather_code': Weather.WEATHER_CODE, 'ym': ym,
                       'instruments': instruments})
    else:
        return render(request, 'climate/main.html', {})


def instrument_details(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    if instrument.siteId.owner.is_active and not instrument.isDeleted:
        isOwner = request.user == instrument.siteId.owner
        return render(request, 'climate/instrument_details.html', {'instrument': instrument, 'isOwner': isOwner})
    else:
        return render(request, 'climate/main.html', {})


@login_required
def instrument_delete(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    if request.user == instrument.siteId.owner:
        instrument.isDeleted = True
        instrument.save()
        return redirect(own_instrument_list)
    else:
        return render(request, 'climate/main.html', {})


def yearly_view(request, pk, year):
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
                                                            'monthNames': monthList, 'num': datasetNum, 'report': a,
                                                            'climate': climate, 'significants': significants})
    else:
        return render(request, 'climate/main.html', {})


def monthly_view(request, site, year, month):
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


def observations(request, pk):
    site = get_object_or_404(Site, pk=pk)
    if (site.isPublic and site.owner.is_active or site.owner == request.user):
        observations = RawObservation.objects.filter(siteId=site).order_by('-createdDate')
        return render(request, 'climate/site_observations.html',
                      {'site': site, 'observations': observations, 'weather_code': Weather.WEATHER_CODE})
    else:
        return render(request, 'climate/main.html', {})


@login_required
def delete_site_image(request, site, number):
    siteObj = get_object_or_404(Site, pk=site)
    if (siteObj.owner == request.user):
        siteObj.primaryImage.delete()
        siteObj.save()
        return redirect(site_edit, pk=site)
    else:
        return render(request, 'climate/main.html', {})


@login_required
def climate(request, pk, year=None, month=None):
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
    for i in this_month.days_of_month_till_today():
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


def process(var):
    if var != "---":
        return int(float(var))


def create_daily_statistics(fromDate, toDate, siteId, limitInMins=10):
    print("daily", fromDate, toDate)
    limit = datetime.timedelta(minutes=(limitInMins))
    fromDate = fromDate.replace(hour=0, minute=0, second=0)
    delta = toDate - fromDate
    for i in range(delta.days + 1):
        print(i)
        f = fromDate + datetime.timedelta(days=i)
        t = fromDate + datetime.timedelta(days=i + 1)
        rawDataSet = RawData.objects.filter(createdDate__year=f.year,
                                            createdDate__month=f.month,
                                            createdDate__day=f.day).filter(siteId=siteId)
        manualDataSet = RawManualData.objects.filter(siteId=siteId).filter(year=f.year).filter(month=f.month).filter(
            day=f.day)
        precipitation = None
        if rawDataSet.count():
            d, created = DailyStatistics.objects.update_or_create(siteId=siteId, year=f.year, month=f.month, day=f.day)
            d.dataAvailable = rawDataSet.count()
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
            d.tempDistribution = ''.join(str(e) + ',' for e in tempDistribution)[:-1]
            rhDistribution = Climate.calculate_rh_distribution(rhs)
            d.rhDistribution = ''.join(str(e) + ',' for e in rhDistribution)[:-1]
            windDistribution = Climate.calculate_wind_distribution(winds)
            d.windDistribution = ''.join(str(e) + ',' for e in windDistribution)[:-1]
            if len(temps) > 0:
                d.tempMin = min(temps)
                d.tempMax = max(temps)
                d.tempAvg = sum(temps) / len(temps)
            if precipitation is not None:
                d.precipitation = precipitation
            d.save()
        if manualDataSet.count():
            d, created = DailyStatistics.objects.update_or_create(siteId=siteId, year=f.year, month=f.month, day=f.day)
            if manualDataSet[0].tMin is not None:
                d.tempMin = manualDataSet[0].tMin
            if manualDataSet[0].tMax is not None:
                d.tempMax = manualDataSet[0].tMax
            if manualDataSet[0].precAmount is not None:
                d.precipitation = manualDataSet[0].precAmount
            d.save()
    return 1


def create_monthly_statistics(fromDate, toDate, siteId):
    fromDate = fromDate.replace(hour=0, minute=0, second=0, day=1)
    if (toDate.month < 12):
        toDate = toDate.replace(month=toDate.month + 1, day=1, hour=0, minute=0, second=0)
    else:
        toDate = toDate.replace(year=toDate.year + 1, month=1, day=1, hour=0, minute=0, second=0)
    f = fromDate
    while f < toDate:

        rawDataSet = DailyStatistics.objects.filter(year=f.year, month=f.month).filter(siteId=siteId)
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
    return 1


def create_yearly_statistics(fromDate, toDate, siteId):
    fromDate = fromDate.replace(month=1, day=1, hour=0, minute=0, second=0)
    toDate = toDate.replace(month=12, day=31, hour=23, minute=59, second=59)
    f = fromDate
    while f < toDate:
        d, created = YearlyStatistics.objects.update_or_create(siteId=siteId, year=f.year)

        manualDataSet = RawManualData.objects.filter(siteId=siteId).filter(year=f.year)
        significants = {}
        for day in manualDataSet:
            significants = Climate.count_significants(significants, day.weatherCode)

        d.significants = significants
        d.save()

        f = f.replace(year=f.year + 1)
    return 1


@login_required
def upload_data(request, pk):
    site = get_object_or_404(Site, pk=pk)
    if site.owner == request.user and site.isActive:
        return render(request, 'climate/upload.html', {'site': site})
    else:
        return render(request, 'climate/main.html', {})


def create_statistics(site, year=None, month=None, limitInMins=10):
    print(site, year, month, limitInMins)
    hasData = False
    if year is not None and month is not None:
        if RawData.objects.filter(siteId=site).filter(createdDate__year=year).filter(
                createdDate__month=month).count() > 0 or RawManualData.objects.filter(siteId=site).filter(
            year=year).filter(month=month).count() > 0:
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
                firstDate2 = datetime.datetime(fd2.year, fd2.month, fd2.day, 0, 0, tzinfo=pytz.timezone("Europe/Budapest"))
                lastDate2 = datetime.datetime(ld2.year, ld2.month, ld2.day, 23, 59, tzinfo=pytz.timezone("Europe/Budapest"))
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
    def post(self, request, *args, **kw):
        print(1)
        logger.debug('POST request at UploadHandler')
        def _saveToDb():
            handle_uploaded_data(site, request.data.get('data', None))

        def _calculateStatistics():
            print("calc", site)
            create_statistics(site)

        if request.user != None and request.user.profile.canUpload:
            if request.data != None and 'site' in request.data:
                site = get_object_or_404(Site, pk=request.data.get('site', None))
                if site.isActive and 'data' in request.data:
                    response = Response(None, status=status.HTTP_204_NO_CONTENT)
                    t = Timer(0, _saveToDb)
                    t.start()
                    if 'isLastPart' in request.data and request.data.get('isLastPart', None):
                        t = Timer(WAIT_BEFORE_CALCULATE_STATISTICS, _calculateStatistics)
                        t.start()
        return response


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
                    if data[i].get('Tmin') is not None:
                        d.tMin = data[i].get('Tmin')
                    if data[i].get('Tmax') is not None:
                        d.tMax = data[i].get('Tmax')
                    if data[i].get('prec') is not None:
                        d.precAmount = data[i].get('prec')
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
            create_statistics(site, year, month)

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


def handle_uploaded_data(site, data):
    start = datetime.datetime.fromtimestamp(data[0].get('date', None) / 1000, tz=pytz.timezone("Europe/Budapest"))
    end = datetime.datetime.fromtimestamp(data[-1].get('date', None) / 1000, tz=pytz.timezone("Europe/Budapest"))
    existing = RawData.objects.filter(createdDate__range=(start, end), siteId=site)
    existing_dates = existing.values_list('createdDate', flat=True)

    RawData.objects.bulk_create(
        RawData(siteId=site,
                createdDate=datetime.datetime.fromtimestamp(line.get('date', None) / 1000,
                                                            tz=pytz.timezone("Europe/Budapest")),
                dewpoint=line.get('dewpoint', None),
                precipitation=line.get('precipitation', None),
                humidity=line.get('relativeHumidity', None),
                pressure=line.get('relativePressure', None),
                humidityIn=line.get('rhIndoor', None),
                tempIn=line.get('tempIndoor', None),
                temperature=line.get('temperature', None),
                windChill=line.get('windChill', None),
                windSpeed=line.get('windSpeed', None),
                windDir=line.get('windDirection', None),
                gust=line.get('windGustSpeed', None)
                )

        for line in data
        if datetime.datetime.fromtimestamp(line.get('date', None) / 1000,
                                           tz=pytz.timezone("Europe/Budapest")) not in existing_dates
    )
