from django.shortcuts import render


def guide(request):
    """
    | Handbook for observations

    :param request: HTTP request
    :return: renders ``climate/guide.html``
    """
    return render(request, 'climate/guide.html')