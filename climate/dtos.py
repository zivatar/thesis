class DTO:
    _default_value = None

    def __init__(self, **kwargs):
        for k in self.__slots__:
            self.__setattr__(k, None)
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class DailyStatisticsDTO(DTO):
    __slots__ = [
        "siteId", "year", "month", "day", "dataAvailable", "tempMin", "tempMax", "tempAvg",
        "precipitation", "precipHalfHour", "tempDistribution", "rhDistribution",
        "windDistribution", "existing"
    ]

    def __init__(self, **kwargs):
        DTO.__init__(self, **kwargs)
