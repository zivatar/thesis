from django.db import models

from climate.classes.Weather import Weather


class RawObservation(models.Model):
    """
    | Raw observation created by a human individual
    | Foreign key to Site objects
    """

    siteId = models.ForeignKey('climate.Site', help_text='foreign key to Site table')
    createdDate = models.DateTimeField(auto_now_add=True, help_text='timestamp')
    comment = models.TextField(blank=True, help_text='comment with free text')
    _weatherCode = models.CommaSeparatedIntegerField(max_length=200, choices=Weather.WEATHER_CODE, blank=True,
                                                     help_text='observed significant weather event')
    windSpeed = models.IntegerField(choices=Weather.BEAUFORT_SCALE, default=0,
                                    help_text='wind speed in Beaufort level, choices=Weather.BEAUFORT_SCALE')

    def populate_weather_code(self, arr):
        """
        | Insert weather codes to the data structure of the table

        :param arr: weather observations
        :type arr: list of Weather.WEATHER_CODE
        :return:
        """
        wc = ''
        for a in arr:
            wc = wc + a + ','
        self._weatherCode = wc
        self.save()

    @property
    def weatherCode(self):
        """
        | Get weather code in readable format

        :return: list of events
        """
        return self.convert_to_readables(self._weatherCode[:-1].split(','))

    @weatherCode.setter
    def weatherCode(self, value):
        """
        | Set weather code

        :param value: CommaSeparatedIntegerField
        :return: None
        """
        self._weatherCode = value

    def convert_to_readables(self, codes):
        """
        | Get the name of weather events

        :param codes: list of codes
        :return: list of names
        """
        out = []
        for o in codes:
            out.append(self.convert_to_readable(o))
        return out

    def convert_to_readable(self, code):
        """
        | Get the name of the weather event

        :param code: weather code
        :return: name
        """
        return Weather.get_weather_code_text(code)
