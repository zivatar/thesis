from django.contrib import admin

from climate.models.DailyStatistics import DailyStatistics
from climate.models.Instrument import Instrument
from climate.models.MonthlyStatistics import MonthlyStatistics
from climate.models.RawData import RawData
from climate.models.RawManualData import RawManualData
from climate.models.RawObservation import RawObservation
from climate.models.Site import Site
from climate.models.YearlyStatistics import YearlyStatistics

admin.site.register(Site)
admin.site.register(Instrument)
admin.site.register(RawData)
admin.site.register(RawObservation)
admin.site.register(RawManualData)
admin.site.register(DailyStatistics)
admin.site.register(MonthlyStatistics)
admin.site.register(YearlyStatistics)
