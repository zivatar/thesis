from django.db import models
from picklefield.fields import PickledObjectField


class YearlyStatistics(models.Model):
    class Meta:
        unique_together = (('siteId', 'year'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField()
    significants = PickledObjectField(default={})
