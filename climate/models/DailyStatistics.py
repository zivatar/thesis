from django.db import models


class DailyStatistics(models.Model):
    class Meta:
        unique_together = (('siteId', 'year', 'month', 'day'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    dataAvailable = models.IntegerField(default=0)
    tempMin = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempMax = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    precipitation = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    precipHalfHour = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    tempDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    rhDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    windDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
