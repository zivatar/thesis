from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from climate.forms import RegistrationForm
from climate.views.main import main


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(main)
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})
