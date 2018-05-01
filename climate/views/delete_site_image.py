from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from climate.models.Site import Site
from climate.views.edit_site import edit_site


@login_required
def delete_site_image(request, site, number):
    siteObj = get_object_or_404(Site, pk=site)
    if siteObj.owner == request.user:
        siteObj.primaryImage.delete()
        siteObj.save()
        return redirect(edit_site, pk=site)
    else:
        return render(request, 'climate/main.html', {})
