from django.shortcuts import get_object_or_404, render

from climate.models.Instrument import Instrument


def instrument_details(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    if instrument.siteId.owner.is_active and not instrument.isDeleted:
        isOwner = request.user == instrument.siteId.owner
        return render(request, 'climate/instrument_details.html', {'instrument': instrument, 'isOwner': isOwner})
    else:
        return render(request, 'climate/main.html', {})

