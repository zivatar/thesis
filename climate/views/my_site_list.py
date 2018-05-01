from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from climate.models.Site import Site


@login_required
def my_site_list(request):
    sites = Site.objects.filter(owner=request.user).filter(isDeleted=False).order_by('title')
    return render(request, 'climate/site_list.html', {'sites': sites})
