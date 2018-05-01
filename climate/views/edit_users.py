from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

from climate.utils import is_admin


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def edit_users(request):
    my_user = request.user
    users = User.objects.all().select_related('profile')
    return render(request, 'climate/edit_users.html', {'user': my_user, 'users': users})
