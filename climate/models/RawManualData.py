from django.db import models

from climate.classes.Weather import Weather


class RawManualData(models.Model):
    """
    Manual data from a day
    """
    class Meta:
        unique_together = (('year', 'month', 'day', 'siteId'),)

    siteId = models.ForeignKey('climate.Site')
    year = models.IntegerField(default=-1)
    month = models.IntegerField(default=-1)
    day = models.IntegerField(default=-1)
    tMin = models.FloatField(blank=True, null=True)
    tMax = models.FloatField(blank=True, null=True)
    precAmount = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True)
    isSnow = models.BooleanField(default=False)
    snowDepth = models.FloatField(default=0.0)
    _weatherCode = models.CommaSeparatedIntegerField(max_length=200, choices=Weather.WEATHER_CODE, blank=True)

    def addWeatherCode(self, code):
        """
        Add weather observation code
        :param code:
        :return:
        """
        weatherCodes = self._weatherCode[:-1].split(',')
        if not code in weatherCodes:
            self._weatherCode = self._weatherCode + code + ','

    def populateWeatherCode(self, arr):
        wc = ''
        for a in arr:
            wc = wc + a + ','
        self._weatherCode = wc
        self.save()

    @property
    def weatherCode(self):
        if len(self._weatherCode[:-1]) > 0:
            return self._weatherCode[:-1].split(',')
        else:
            return []

    @weatherCode.setter
    def weatherCode(self, value):
        self._weatherCode = value
