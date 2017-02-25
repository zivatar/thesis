from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Site, WIDE_AREA, NARROW_AREA

def site_list(request):
	sites = Site.objects.filter(isPublic=True).order_by('title')
	return render(request, 'climate/site_list.html', {'sites': sites})
	
@login_required
def my_sites(request):
	sites = Site.objects.filter(owner=request.user)
	return render(request, 'climate/my_sites.html', {'sites': sites, 'wide_area': WIDE_AREA, 'narrow_area': NARROW_AREA})
	
def main(request):
	return render(request, 'climate/main.html', {})