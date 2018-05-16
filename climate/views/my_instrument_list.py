from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from climate.models.Instrument import Instrument


@login_required
def my_instrument_list(request):
    """
    | List of the instruments of the user
    | Login required

    :param request: HTTP request
    :return: renders ``climate/instrument_list.html``
    """
    instruments = Instrument.objects.filter(siteId__owner=request.user).filter(isDeleted=False).order_by('title')
    return render(request, 'climate/instrument_list.html', {'instruments': instruments})
