from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from climate.models.Instrument import Instrument
from climate.views.my_instrument_list import my_instrument_list


@login_required
def delete_instrument(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    if request.user == instrument.siteId.owner:
        instrument.isDeleted = True
        instrument.save()
        return redirect(my_instrument_list)
    else:
        return render(request, 'climate/main.html', {})
