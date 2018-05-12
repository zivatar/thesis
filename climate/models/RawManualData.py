from django.db import models

from climate.classes.Weather import Weather


class RawManualData(models.Model):
    """
    Manual data from a day
    """
    class Meta:
        unique_together = (('year', 'month', 'day', 'siteId'),)

    siteId = models.ForeignKey('climate.Site', help_text='foreign key for Site table')
    year = models.IntegerField(default=-1)
    month = models.IntegerField(default=-1)
    day = models.IntegerField(default=-1)
    tMin = models.FloatField(blank=True, null=True, help_text='daily temperature minimum (°C)')
    tMax = models.FloatField(blank=True, null=True, help_text='daily temperature maximum (°C)')
    precAmount = models.FloatField(blank=True, null=True, help_text='daily amount of precipitation (mm)')
    comment = models.TextField(blank=True)
    isSnow = models.BooleanField(default=False, help_text='is there snow cover')
    snowDepth = models.FloatField(default=0.0, help_text='snow depth (cm)')
    _weatherCode = models.CommaSeparatedIntegerField(max_length=200, choices=Weather.WEATHER_CODE,
                                                     blank=True,
                                                     help_text='list of existing significant events')

    def addWeatherCode(self, code):
        """
        | Add weather observation code to its list

        :param code: weather code
        :type code: tuple
        :return: None
        """
        weatherCodes = self._weatherCode[:-1].split(',')
        if not code in weatherCodes:
            self._weatherCode = self._weatherCode + code + ','

    def populateWeatherCode(self, arr):
        """
        | Parses a list containing weather codes into its weather code property

        :param arr: list of weather codes
        :type arr: list
        :return: None
        """
        wc = ''
        for a in arr:
            wc = wc + a + ','
        self._weatherCode = wc
        self.save()

    @property
    def weatherCode(self):
        """
        | Getter of weatherCode property

        :return: list of weather codes
        """
        if len(self._weatherCode[:-1]) > 0:
            return self._weatherCode[:-1].split(',')
        else:
            return []

    @weatherCode.setter
    def weatherCode(self, value):
        """
        | Setter of weatherCode property

        :param value:
        :return: CommaSeparatedIntegerField
        """
        self._weatherCode = value
