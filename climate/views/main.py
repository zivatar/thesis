from django.shortcuts import render


def main(request):
    """
    Main page of the site

    :param request: HTTP request
    :return: renders ``climate/main.html``
    """
    return render(request, 'climate/main.html', {})
