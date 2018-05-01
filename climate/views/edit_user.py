from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from climate.classes.Gravatar import Gravatar
from climate.forms import UserForm
from climate.utils import is_admin
from climate.views.edit_users import edit_users


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def edit_user(request, user):
    user_obj = get_object_or_404(User, pk=user)
    gravatar = Gravatar.get_gravatar_url(user_obj.email)
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_obj.is_active = cd.get('isActive')
            user_obj.is_superuser = cd.get('isAdmin')
            user_obj.profile.canUpload = cd.get('canUpload')
            user_obj.save()
            return redirect(edit_users)
    else:
        form = UserForm(initial={"isAdmin": is_admin(user_obj), "isActive": user_obj.is_active,
                                 "canUpload": user_obj.profile.canUpload})
    return render(request, 'climate/edit_user.html', {'editUser': user_obj, 'form': form, 'gravatar': gravatar})
