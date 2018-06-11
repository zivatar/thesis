from django.shortcuts import render

from climate.models.Site import Site


def public_site_list(request):
    """
    Public site list

    :param request: HTTP request
    :return: renders ``climate/site_list.html``
    """
    print("public site list")
    sites = Site.objects.filter(isPublic=True).filter().order_by('title')
    return render(request, 'climate/site_list.html', {'sites': sites})
