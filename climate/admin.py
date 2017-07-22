from django.contrib import admin
from .models import Site, Instrument, RawData, RawObservation, RawManualData
from .models import DailyStatistics, MonthlyStatistics

admin.site.register(Site)
admin.site.register(Instrument)
admin.site.register(RawData)
admin.site.register(RawObservation)
admin.site.register(RawManualData)

admin.site.register(DailyStatistics)
admin.site.register(MonthlyStatistics)