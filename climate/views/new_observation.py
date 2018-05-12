from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from climate.classes.Weather import Weather
from climate.forms import ObservationForm
from climate.models.RawManualData import RawManualData
from climate.models.Site import Site
from climate.views.main import main


@login_required
def new_observation(request):
    sites = Site.objects.filter(owner=request.user)
    if request.method == "POST":
        form = ObservationForm(request.POST)
        if form.is_valid():
            obs = form.save()
            weather_codes = form.cleaned_data.get('weatherCode')
            obs.populate_weather_code(weather_codes)
            daily_data, created = RawManualData.objects.update_or_create(year=obs.createdDate.year,
                                                                         month=obs.createdDate.month,
                                                                         siteId=obs.siteId,
                                                                         day=obs.createdDate.day)
            for code in weather_codes:
                daily_data.addWeatherCode(code)
                daily_data.save()
            create_statistics(site=obs.siteId, year=obs.createdDate.year, month=obs.createdDate.month)
            return redirect(main)
    else:
        form = ObservationForm()
    return render(request, 'climate/new_observation.html',
                  {'sites': sites, 'form': form, 'wind_speed': Weather.BEAUFORT_SCALE,
                   'weather_code': Weather.WEATHER_CODE})
