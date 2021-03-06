from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from climate.classes.Gravatar import Gravatar


@login_required
def my_user(request):
    """
    | Show data sheet of a user
    | ``@login_required``

    :param request: HTTP request
    :return: renders ``climate/my_user.html``
    """
    user = request.user
    gravatar = Gravatar.get_gravatar_url(user.email)
    return render(request, 'climate/my_user.html', {'user': user, 'gravatar': gravatar})