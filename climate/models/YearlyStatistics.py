from django.db import models
from picklefield.fields import PickledObjectField


class YearlyStatistics(models.Model):
    """
    | Yearly statistics
    | Unique: siteId, year
    """
    class Meta:
        unique_together = (('siteId', 'year'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField()
    significants = PickledObjectField(default={})
