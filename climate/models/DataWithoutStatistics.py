from django.db import models


class DataWithoutStatistics(models.Model):
    siteId = models.ForeignKey('climate.Site')
    fromYear = models.IntegerField()
    fromMonth = models.IntegerField()
    toYear = models.IntegerField()
    toMonth = models.IntegerField()
    uploadedAt = models.DateTimeField()