from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from climate.forms import InstrumentForm
from climate.models.Site import Site
from climate.views import my_instrument_list


@login_required
def new_instrument(request):
    """
    | Form for creating a new instrument
    | ``@login_required``

    :param request: HTTP request
    :return: renders ``climate/new_instrument.html``
    """
    sites = Site.objects.filter(owner=request.user)
    if request.method == "POST":
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
            return redirect(my_instrument_list)
    else:
        form = InstrumentForm()
    return render(request, 'climate/new_instrument.html', {'sites': sites, 'form': form})
