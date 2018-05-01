from django.shortcuts import render


def guide(request):
    return render(request, 'climate/guide.html')