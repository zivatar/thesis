from django.db import models
from picklefield.fields import PickledObjectField


class MonthlyStatistics(models.Model):
    """
    | Yearly statistics
    | Unique: year, month, siteId
    | Foreign key to Site objects
    """
    class Meta:
        unique_together = (('year', 'month', 'siteId'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField()
    month = models.IntegerField()
    dataAvailable = models.IntegerField(default=0)
    tempMin = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempMax = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    precipitation = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    tempMinAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    tempMaxAvg = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    summerDays = models.IntegerField(blank=True, null=True)
    frostDays = models.IntegerField(blank=True, null=True)
    winterDays = models.IntegerField(blank=True, null=True)
    coldDays = models.IntegerField(blank=True, null=True)
    warmNights = models.IntegerField(blank=True, null=True)
    warmDays = models.IntegerField(blank=True, null=True)
    hotDays = models.IntegerField(blank=True, null=True)
    tempDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    rhDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    windDistribution = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    significants = PickledObjectField(default={})
