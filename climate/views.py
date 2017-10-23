from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .classes.weather import Weather
from .models import Site, Climate, Instrument
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import gravatar as gr


monthList = ['J', 'F', 'M', 'Á', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']

def is_admin(user):
	if user:
		return user.groups.filter(name='is_admin').exists()
	return False

def can_upload(user):
	if user:
		return user.groups.filter(name='can_upload').exists()
	return False

def site_list(request):
	sites = Site.objects.filter(isPublic=True).filter().order_by('title')
	return render(request, 'climate/site_list.html', {'sites': sites})

@login_required
def own_site_list(request):
	sites = Site.objects.filter(owner=request.user).order_by('title')
	return render(request, 'climate/site_list.html', {'sites': sites})

@login_required
def own_instrument_list(request):
	instruments = Instrument.objects.filter(owner=request.user).order_by('title')
	return render(request, 'climate/instrument_list.html', {'instruments': instruments})

@login_required
def new_instrument(request):
	sites = Site.objects.filter(owner=request.user)
	if request.method == "POST":
		form = InstrumentForm(request.POST)
		if form.is_valid():
			inst = form.save(commit=False)
			inst.owner = request.user
			inst.save()
			return redirect(own_instrument_list)
	else:
		form = InstrumentForm()
	return render(request, 'climate/new_instrument.html', {'sites': sites, 'form': form })

@login_required
def my_user(request):
	user = request.user
	gravatar = gr.gravatar_url(user.email)
	return render(request, 'climate/my_user.html', {'user': user, 'gravatar': gravatar})

@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def edit_users(request):
	myUser = request.user
	users = User.objects.filter()
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
			userObj.groups.clear()
			if cd.get('isAdmin'):
				g = Group.objects.get(name='is_admin') 
				userObj.groups.add(g)
			if cd.get('canUpload'):
				g = Group.objects.get(name='can_upload') 
				userObj.groups.add(g)
			userObj.save()
			return redirect(edit_users)
	else:
		form = UserForm(initial={"isAdmin": is_admin(userObj), "isActive": userObj.is_active, "canUpload": can_upload(userObj)})
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
	return render(request, 'climate/new_site.html', {'sites': sites, 'wide_area': Site.WIDE_AREA, 'narrow_area': Site.NARROW_AREA, 'form': form})

@login_required
def new_observation(request):
	sites = Site.objects.filter(owner=request.user)
	if request.method == "POST":
		form = ObservationForm(request.POST)
		if form.is_valid():
			obs = form.save()
			weatherCodes = form.cleaned_data.get('weatherCode')
			obs.populateWeatherCode(weatherCodes)
			return redirect(main)
	else:
		form = ObservationForm()
	return render(request, 'climate/new_observation.html', {'sites': sites, 'form': form, 'wind_speed': Weather.BEAUFORT_SCALE, 'weather_code': Weather.WEATHER_CODE})
	
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
	if (site.isPublic and site.owner.is_active or site.owner == request.user):
		observations = RawObservation.objects.filter(siteId = site).order_by('-createdDate')[:3]
		yearly = YearlyStatistics.objects.filter(siteId = site)
		monthly = MonthlyStatistics.objects.filter(siteId = site)
		ym = createYearlyMonthly(yearly, monthly)
		instruments = Instrument.objects.filter(siteId = site).order_by('title')
		return render(request, 'climate/site_details.html', {'site' : site, 'observations' : observations, 'weather_code': Weather.WEATHER_CODE, 'ym': ym, 'instruments': instruments})
	else:
		return render(request, 'climate/main.html', {})

def instrument_details(request, pk):
	instrument = get_object_or_404(Instrument, pk=pk)
	if instrument.owner.is_active:
		return render(request, 'climate/instrument_details.html', {'instrument': instrument})
	else:
		return render(request, 'climate/main.html', {})

def yearly_view(request, pk, year):
	site = get_object_or_404(Site, pk=pk)
	yearlyList = YearlyStatistics.objects.filter(siteId = site).filter(year = year)
	if len(yearlyList) > 0:
		yearly = yearlyList[0]
	monthly = MonthlyStatistics.objects.filter(siteId = site).filter(year = year)
	if site and yearlyList and monthly and (site.isPublic and site.owner.is_active or site.owner == request.user):
		climate = {'temp': Climate().tempDistribLimits, 'wind': Climate().windDirLimits, 'rh': Climate().rhDistribLimits}
		datasetNum = []
		for i in range(12):
			added = False
			for j in monthly:
				if j.month == i + 1:
					datasetNum.append({'id': i+1, 'available':j.dataAvailable})
					added = True
			if not added:
				datasetNum.append({'id': i+1, 'available':0})
		a = YearlyReport(site, year, monthly, yearly)
		return render(request, 'climate/yearly_view.html', {'site' : site, 'year': yearly, 'monthNames': monthList, 'num': datasetNum, 'report': a, 'climate': climate})
	else:
		return render(request, 'climate/main.html', {})

def monthly_view(request, site, year, month):
	siteObj = get_object_or_404(Site, pk=site)
	yearly = YearlyStatistics.objects.filter(siteId = siteObj).filter(year = year)
	monthly = MonthlyStatistics.objects.filter(siteId = siteObj).filter(year = year).filter(month = month)
	daily = DailyStatistics.objects.filter(siteId = siteObj).filter(date__year = year).filter(date__month = month)
	if siteObj and yearly and monthly and daily and (siteObj.isPublic and siteObj.owner.is_active or siteObj.owner == request.user):
		climate = {'temp': Climate().tempDistribLimits, 'wind': Climate().windDirLimits, 'rh': Climate().rhDistribLimits}
		datasetNum = []
		a = MonthlyReport(site, year, month, monthly, yearly, daily)
		return render(request, 'climate/monthly_view.html', {'site' : siteObj, 'num': datasetNum, 'year': yearly, 'month': month, 'report': a, 'climate': climate})
	else:
		return render(request, 'climate/main.html', {})

def observations(request, pk):
	site = get_object_or_404(Site, pk=pk)
	if (site.isPublic and site.owner.is_active or site.owner == request.user):
		observations = RawObservation.objects.filter(siteId = site).order_by('-createdDate')
		return render(request, 'climate/site_observations.html', {'site' : site, 'observations' : observations, 'weather_code': Weather.WEATHER_CODE})
	else:
		return render(request, 'climate/main.html', {})

@login_required
def delete_site_image(request, site, number):
	print(number, number == 1, type(number), type(1))
	siteObj = get_object_or_404(Site, pk=site)
	if (siteObj.owner == request.user):
		if (number == '1'):
			siteObj.primaryImage.delete()
		else:
			siteObj.secondaryImage.delete()
		siteObj.save()
		return redirect(site_edit, pk=site)
	else:
		return render(request, 'climate/main.html', {})

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
		return render(request, 'climate/site_edit.html', {'sites': sites, 'wide_area': Site.WIDE_AREA, 'narrow_area': Site.NARROW_AREA, 'form': form, 'site': site})
	else:
		return render(request, 'climate/main.html', {})

@login_required
def climate(request, pk):
	site = get_object_or_404(Site, pk=pk)
	return render(request, 'climate/climate.html', {'site': site})


# TODO remove
@login_required
def actual_month(request, pk):
	site = get_object_or_404(Site, pk=pk)
	thisMonth = Month()
	actuals = RawManualData.objects.filter(year = thisMonth.year, month = thisMonth.month) # siteId = site, 
	if request.method == "POST":
		form = DiaryForm(request.POST)
		if form.is_valid():
			diary = form.save(commit=False)
			diary.year = thisMonth.year
			diary.month = thisMonth.month
			print (form)
			diary.siteId = site
			diary.save()
			return redirect(actual_month, pk)
	else:
		form = DiaryForm()
	return render(request, 'climate/actual_month.html', {'site' : site, 'month': thisMonth, 'weather_code': Weather.WEATHER_CODE, 'form': form, 'actuals': actuals })

def process(var):
	if var != "---":
		return int(float(var))

def handle_uploaded_file(f, site):
	lineNumber = 0
	for line in f:
		line = line.decode('cp437')
		lineNumber = lineNumber + 1
		if lineNumber > 1:
			#data = RawData()
			
			line = sub('"', '', line).split(';')
			date = line[1]
			
			#data.siteId = site
			#data.createdDate = dtparser.parse(date + "+0100")
			
			#book = Book.objects.create(title="Ulysses")
			data, created = RawData.objects.get_or_create(siteId = site, createdDate = dtparser.parse(date + "+0100"))
			
			if lineNumber == 2:
				firstDate = dtparser.parse(date + "+0100")
			lastDate = dtparser.parse(date + "+0100")
			
			if created:
				if process(line[2]):
					data.pressure = process(line[2])
				if process(line[3]):
					data.tempIn = process(line[3])
				if process(line[4]):
					data.humidityIn = process(line[4])
				if process(line[5]):
					data.temperature = process(line[5])
				if process(line[6]):
					data.humidity = process(line[6])
				if process(line[7]):
					data.dewpoint = process(line[7])
				if process(line[8]):
					data.windChill = process(line[8])
				if process(line[9]):
					data.windSpeed = process(line[9])
				if process(line[10]):
					data.windDir = process(line[10])
				if process(line[11]):
					data.gust = process(line[11])
				if process(line[12]):
					data.precipitation = process(line[12])
				data.save()
	return firstDate, lastDate

def create_daily_statistics(fromDate, toDate, siteId):
	# nyari nap, hosegnap, stb
	# fel oras csapadekosszeg maximuma
	# jelentos csapadek volt-el
	#
	fromDate = fromDate.replace(hour=0, minute=0, second=0)
	delta = toDate - fromDate
	for i in range(delta.days + 1):
		newObj = False
		f = fromDate + datetime.timedelta(days = i)
		d = DailyStatistics.objects.filter(siteId = siteId, date=f)
		if len(d) == 0:
			d = DailyStatistics()
		else:
			d = d[0]
		d.date = f
		t = fromDate + datetime.timedelta(days = i + 1)
		rawDataSet1 = RawData.objects.filter(siteId = siteId)
		rawDataSet = RawData.objects.filter(createdDate__year=f.year, 
							createdDate__month=f.month, 
							createdDate__day=f.day).filter(siteId = siteId)
		d.dataAvailable = rawDataSet.count()
		tempMin = decimal.Decimal(99.9)
		tempMax = decimal.Decimal(-99.9)
		tempSum = decimal.Decimal(0.0)
		tempNum = decimal.Decimal(0.0)
		temps = []
		rhs = []
		winds = []
		precipitation = decimal.Decimal(0.0)
		for j in rawDataSet:
			if j.temperature is not None:
				tempSum = tempSum + j.temperature
				tempNum = tempNum + 1
				if j.temperature < tempMin:
					tempMin = j.temperature
				if j.temperature > tempMax:
					tempMax = j.temperature
				temps.append(j.temperature)
			if j.humidity is not None:
				rhs.append(j.humidity)
			if j.precipitation is not None:
				precipitation = precipitation + j.precipitation
			if j.windDir is not None:
				winds.append(j.windDir)
		tempDistribution = Climate.calculateTempDistrib(temps)
		d.tempDistribution = ''.join(str(e)+',' for e in tempDistribution)[:-1]
		rhDistribution = Climate.calculateRhDistrib(rhs)
		d.rhDistribution = ''.join(str(e)+',' for e in rhDistribution)[:-1]
		windDistribution = Climate.calculateWindDistrib(winds)
		d.windDistribution = ''.join(str(e)+',' for e in windDistribution)[:-1]
		d.tempMin = tempMin
		d.tempMax = tempMax
		d.tempAvg = tempSum / tempNum
		d.precipitation = precipitation
		d.save()
	return 1

def create_monthly_statistics(fromDate, toDate, siteId):
	fromDate = fromDate.replace(hour=0, minute=0, second=0, day=1)
	toDate = toDate.replace(month=toDate.month+1, day=1, hour=0, minute=0, second=0)
	f = fromDate
	while f < toDate:
		d = MonthlyStatistics.objects.filter(siteId = siteId, month = f.month, year = f.year)
		if len(d) == 0:
			d = MonthlyStatistics()
			d.month = f.month
			d.year = f.year
			d.siteId = siteId
		else:
			d = d[0]
		rawDataSet = DailyStatistics.objects.filter(date__year=f.year, 
							date__month=f.month).filter(siteId = siteId)
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
							createdDate__month=f.month).filter(siteId = siteId)
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
		tempDistribution = Climate.calculateTempDistrib(temps)
		d.tempDistribution = ''.join(str(e)+',' for e in tempDistribution)[:-1]
		rhDistribution = Climate.calculateRhDistrib(rhs)
		d.rhDistribution = ''.join(str(e)+',' for e in rhDistribution)[:-1]
		windDistribution = Climate.calculateWindDistrib(winds)
		d.windDistribution = ''.join(str(e)+',' for e in windDistribution)[:-1]
		d.precipitation = precipitation
		d.summerDays = Climate.getNrSummerDays(tempmaxs)
		d.frostDays = Climate.getNrFrostDays(tempmins)
		d.coldDays = Climate.getNrColdDays(tempmins)
		d.warmNights = Climate.getNrWarmNights(tempmins)
		d.warmDays = Climate.getNrWarmDays(tempmaxs)
		d.hotDays = Climate.getNrHotDays(tempmaxs)
		d.save()
		f = f.replace(month = f.month + 1)
	return 1

def create_yearly_statistics(fromDate, toDate, siteId):
	fromDate = fromDate.replace(month = 1, day = 1, hour = 0, minute = 0, second = 0)
	toDate = toDate.replace(month = 12, day = 31, hour = 23, minute = 59, second = 59)
	f = fromDate
	while f < toDate:
		print(f)
		d = YearlyStatistics.objects.filter(siteId = siteId, year = f.year)
		if len(d) == 0:
			d = YearlyStatistics()
			d.year = f.year
			d.siteId = siteId
		else:
			d = d[0]
		d.save()
		f = f.replace(year = f.year + 1)
	return 1
	
@login_required
def upload(request, pk):
	site = get_object_or_404(Site, pk=pk)
	if site.owner == request.user:
		if request.method == "POST":
			firstDate, lastDate = handle_uploaded_file(request.FILES['myfile'], site)
			create_daily_statistics(firstDate, lastDate, site)
			create_monthly_statistics(firstDate, lastDate, site)
			create_yearly_statistics(firstDate, lastDate, site)
			return redirect(site_details, pk)
		else:
			return render(request, 'climate/upload.html', {'site': site})
	else:
		return render(request, 'climate/main.html', {})

#@user_passes_test(can_upload)
class UploadHandler(APIView):
	def get(self, request, *args, **kw):
		print("asdfg")
		get_arg1 = request.GET.get('arg1', None)
		get_arg2 = request.GET.get('arg2', None)
		result = 999
		response = Response(result, status=status.HTTP_200_OK)
		return response
	def post(self, request, *args, **kw):
		print("asdfg")
		get_arg1 = request.GET.get('arg1', None)
		get_arg2 = request.GET.get('arg2', None)
		result = 999
		response = Response(result, status=status.HTTP_200_OK)
		return response