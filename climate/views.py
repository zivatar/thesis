from django.shortcuts import render
from .models import Site

def site_list(request):
	sites = Site.objects.all()
	return render(request, 'climate/site_list.html', {'sites': sites})
	
def main(request):
	return render(request, 'climate/main.html', {})