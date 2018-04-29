from django.db import models

from climate.classes.weather import Weather


class RawObservation(models.Model):
    siteId = models.ForeignKey('climate.Site')
    createdDate = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    _weatherCode = models.CommaSeparatedIntegerField(max_length=200, choices=Weather.WEATHER_CODE, blank=True)
    windSpeed = models.IntegerField(choices=Weather.BEAUFORT_SCALE, default=0)

    def populateWeatherCode(self, arr):
        wc = ''
        for a in arr:
            wc = wc + a + ','
        self._weatherCode = wc
        self.save()

    @property
    def weatherCode(self):
        return self.convertToReadables(self._weatherCode[:-1].split(','))

    @weatherCode.setter
    def weatherCode(self, value):
        self._weatherCode = value

    def convertToReadables(self, codes):
        out = []
        for o in codes:
            out.append(self.convertToReadable(o))
        return out

    def convertToReadable(self, code):
        return Weather.get_weather_code_text(code)
