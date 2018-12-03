from decouple import config


def ctx(request):
    return {"GOOGLE_MAPS_API_KEY": config('GOOGLE_MAPS_API_KEY')}
