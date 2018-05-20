from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from climate.forms import SiteForm
from climate.models.Site import Site
from climate.views.my_site_list import my_site_list


@login_required
def new_site(request):
    """
    Renders SiteForm for creating a new site

    :param request: HTTP request
    :return: renders ``climate/new_site.html``
    """
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.owner = request.user
            site.save()
            return redirect(my_site_list)
    else:
        form = SiteForm()
        sites = Site.objects.filter(owner=request.user)
    return render(request, 'climate/new_site.html',
                  {'sites': sites, 'wide_area': Site.WIDE_AREA, 'narrow_area': Site.NARROW_AREA, 'form': form})
