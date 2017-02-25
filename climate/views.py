from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Site

def site_list(request):
	sites = Site.objects.filter(isPublic=True).order_by('title')
	return render(request, 'climate/site_list.html', {'sites': sites})
	
@login_required
def my_sites(request):
	sites = Site.objects.filter(owner=request.user)
	return render(request, 'climate/my_sites.html', {'sites': sites})
	
def main(request):
	return render(request, 'climate/main.html', {})