from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import WIDE_AREA, NARROW_AREA
from .models import Site
from .forms import SiteForm

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
	return render(request, 'climate/new_site.html', {'sites': sites, 'wide_area': WIDE_AREA, 'narrow_area': NARROW_AREA, 'form': form})
	
def main(request):
	return render(request, 'climate/main.html', {})
	
def site_details(request, pk):
	site = get_object_or_404(Site, pk=pk)
	return render(request, 'climate/site_details.html', {'site' : site})

def site_edit(request, pk):
	site = get_object_or_404(Site, pk=pk)
	if request.method == "POST":
		form = SiteForm(request.POST, instance=site)
		if form.is_valid():
			site = form.save(commit=False)
			#site.owner = request.user
			site.save()
			return redirect(site_edit, pk=site.pk)
	else:
		form = SiteForm()
		sites = Site.objects.filter(owner=request.user)
	return render(request, 'climate/site_edit.html', {'sites': sites, 'wide_area': WIDE_AREA, 'narrow_area': NARROW_AREA, 'form': form, 'site': site})
