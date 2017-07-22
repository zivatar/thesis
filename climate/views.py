from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Site, Weather, RawObservation, RawManualData, Month, RawData
from .models import DailyStatistics, MonthlyStatistics
from .forms import SiteForm, ObservationForm, DiaryForm
from django.utils import timezone
from re import sub
from datetime import datetime
import dateutil.parser as dtparser
import calendar
import datetime
import decimal

def site_list(request):
	sites = Site.objects.filter(isPublic=True).order_by('title')
	return render(request, 'climate/site_list.html', {'sites': sites})
	
#@login_required
#def my_sites(request):
#	sites = Site.objects.filter(owner=request.user)
#	return render(request, 'climate/my_sites.html', {'sites': sites, 'wide_area': WIDE_AREA, 'narrow_area': NARROW_AREA})

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
	
def site_details(request, pk):
	site = get_object_or_404(Site, pk=pk)
	observations = RawObservation.objects.filter(siteId = site).order_by('-createdDate')[:3]  
	return render(request, 'climate/site_details.html', {'site' : site, 'observations' : observations, 'weather_code': Weather.WEATHER_CODE})
	
def observations(request, pk):
	site = get_object_or_404(Site, pk=pk)
	observations = RawObservation.objects.filter(siteId = site).order_by('-createdDate')
	return render(request, 'climate/site_observations.html', {'site' : site, 'observations' : observations, 'weather_code': Weather.WEATHER_CODE})

@login_required
def site_edit(request, pk):
	site = get_object_or_404(Site, pk=pk)
	if request.method == "POST":
		form = SiteForm(request.POST, instance=site)
		if form.is_valid():
			site = form.save(commit=False)
			site.save()
			return redirect(site_edit, pk=site.pk)
	else:
		form = SiteForm()
		sites = Site.objects.filter(owner=request.user)
	return render(request, 'climate/site_edit.html', {'sites': sites, 'wide_area': Site.WIDE_AREA, 'narrow_area': Site.NARROW_AREA, 'form': form, 'site': site})

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
		precipitation = decimal.Decimal(0.0)
		for j in rawDataSet:
			if j.temperature is not None:
				tempSum = tempSum + j.temperature
				tempNum = tempNum + 1
				if j.temperature < tempMin:
					tempMin = j.temperature
				if j.temperature > tempMax:
					tempMax = j.temperature
			if j.precipitation is not None:
				precipitation = precipitation + j.precipitation
		d.tempMin = tempMin
		d.tempMax = tempMax
		d.tempAvg = tempSum / tempNum
		d.precipitation = precipitation
		d.save()
	return 1

def create_monthly_statistics(fromDate, toDate, siteId):
	fromDate = fromDate.replace(hour=0, minute=0, second=0, day=1)
	delta = toDate - fromDate
	for i in range(delta.days + 1):
		newObj = False
		f = fromDate + datetime.timedelta(days = i)
		d = MonthlyStatistics.objects.filter(siteId = siteId, month = f.month, year = f.year)
		if len(d) == 0:
			d = MonthlyStatistics()
			d.month = f.month
			d.year = f.year
			d.siteId = siteId
		else:
			d = d[0]
		t = fromDate + datetime.timedelta(days = i + 1)
		rawDataSet = DailyStatistics.objects.filter(date__year=f.year, 
							date__month=f.month).filter(siteId = siteId)
		d.dataAvailable = rawDataSet.count()
		d.summerDays = 0
		d.save()
	return 1
	
@login_required
def upload(request, pk):
	site = get_object_or_404(Site, pk=pk)
	if request.method == "POST":
		firstDate, lastDate = handle_uploaded_file(request.FILES['myfile'], site)
		create_daily_statistics(firstDate, lastDate, site)
		create_monthly_statistics(firstDate, lastDate, site)
		return redirect(site_details, pk)
	else:
		return render(request, 'climate/upload.html', {'site': site})