from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from climate.models.Site import Site


@login_required
def upload_data(request, pk):
    site = get_object_or_404(Site, pk=pk)
    if site.owner == request.user and site.isActive:
        return render(request, 'climate/upload.html', {'site': site})
    else:
        return render(request, 'climate/main.html', {})
