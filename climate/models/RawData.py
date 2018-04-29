from django.db import models


class RawData(models.Model):
    class Meta:
        unique_together = (('siteId', 'createdDate'),)

    siteId = models.ForeignKey('climate.Site')
    createdDate = models.DateTimeField()
    pressure = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=1)
    tempIn = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    humidityIn = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    temperature = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    humidity = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    dewpoint = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    windChill = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    windSpeed = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    windDir = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    gust = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    precipitation = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
