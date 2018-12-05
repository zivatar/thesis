from django.shortcuts import get_object_or_404, render

from climate.models.Instrument import Instrument


def instrument_details(request, pk):
    """
    | Display metadata of an instrument

    :param request: HTTP request
    :param pk: primary key of an instrument
    :return: for a not deleted instrument of an active site renders ``climate/instrument_details.html``, \
    else renders main page (``climate/main.html``)
    """
    instrument = get_object_or_404(Instrument, pk=pk)
    if instrument.siteId.owner.is_active:
        isOwner = request.user == instrument.siteId.owner
        return render(request, 'climate/instrument_details.html', {'instrument': instrument, 'isOwner': isOwner})
    else:
        return render(request, 'climate/main.html', {})

