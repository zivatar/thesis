from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from climate.models.Site import Site
from climate.views.edit_site import edit_site


@login_required
def delete_site_image(request, site):
    """
    | Delete site image
    | Login required

    :param request: HTTP request
    :param site: primary key of site
    :return: for the owner, delete image and redirect to :func:`climate.views.edit_site` \
    for others render main page (``climate/main.html``)
    """
    siteObj = get_object_or_404(Site, pk=site)
    if siteObj.owner == request.user:
        siteObj.primaryImage.delete()
        siteObj.save()
        return redirect(edit_site, pk=site)
    else:
        return render(request, 'climate/main.html', {})
