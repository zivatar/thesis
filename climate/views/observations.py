from django.shortcuts import get_object_or_404, render

from climate.classes.Weather import Weather
from climate.models.RawObservation import RawObservation
from climate.models.Site import Site


def observations(request, pk):
    site = get_object_or_404(Site, pk=pk)
    if site.isPublic and site.owner.is_active or site.owner == request.user:
        observations = RawObservation.objects.filter(siteId=site).order_by('-createdDate')
        return render(request, 'climate/site_observations.html',
                      {'site': site, 'observations': observations, 'weather_code': Weather.WEATHER_CODE})
    else:
        return render(request, 'climate/main.html', {})
