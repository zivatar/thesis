from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from climate.forms import SiteForm
from climate.models.Site import Site


@login_required
def edit_site(request, pk):
    site = get_object_or_404(Site, pk=pk)
    if site.owner == request.user:
        if request.method == "POST":
            form = SiteForm(request.POST, request.FILES, instance=site)
            if form.is_valid():
                site = form.save(commit=False)
                site.save()
                return redirect(edit_site, pk=site.pk)
        else:
            form = SiteForm()
            sites = Site.objects.filter(owner=request.user)
        return render(request, 'climate/site_edit.html',
                      {'sites': sites, 'wide_area': Site.WIDE_AREA, 'narrow_area': Site.NARROW_AREA,
                       'form': form,
                       'site': site})
    else:
        return render(request, 'climate/main.html', {})
