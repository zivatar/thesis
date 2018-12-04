import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from climate.models.Site import Site

logger = logging.getLogger(__name__)

@login_required
def my_site_list(request):
    """
    | List of all non-deleted sites of a user
    | Login is required

    :param request: HTTP request
    :return: renders ``climate/site_list.html``
    """
    logger.info("my site list")
    sites = Site.objects.filter(owner=request.user).filter(isDeleted=False).order_by('title')
    return render(request, 'climate/site_list.html', {'sites': sites})
