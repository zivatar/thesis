import calendar
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Month:
    """
    | Utilities for handling months
    """
    def __init__(self, now=datetime.now(), year=0, month=0):
        if year == 0 or month == 0:
            self.year = now.year
            self.month = now.month
            self._currentMonth = True
        else:
            self.year = int(year)
            self.month = int(month)
            self._currentMonth = False

    def __str__(self):
        return "Month [{}-{}]".format(self.year, self.month, self._currentMonth)

    def __repr__(self):
        return self.__str__()

    def get_date_readable(self):
        """
        | Get date in readable format

        :return: YYYY.MM.
        """
        return str(self.year) + "." + str(self.month).zfill(2) + "."

    def is_in_month(self, timestamp):
        """
        | Is a given timestamp in this month

        :param timestamp: datetime
        :return: boolean
        """
        return self.year == timestamp.year and self.month == timestamp.month

    def get_last_day(self):
        """
        | Get the last day of this month

        :return: index of the last day
        """
        return calendar.monthrange(self.year, self.month)[1]

    def get_days_of_month(self):
        """
        | Get a list with the days of this month

        :return: indices of the days of month
        """
        last_day = calendar.monthrange(self.year, self.month)[1]
        a = []
        [a.append(i) for i in range(1, last_day + 1)]
        return a

    def get_days_of_month_till_today(self):
        """
        | Get a list with the days of this month
        | Does not return days in the real-time future

        :return: indices of the days of month
        """
        if self._currentMonth:
            last_day = datetime.now().day
        else:
            last_day = calendar.monthrange(self.year, self.month)[1]
        a = []
        [a.append(i) for i in range(1, last_day + 1)]
        return a

    def get_month_two_digits(self):
        """
        | Get the number of the month in human readable format with two digits

        :return: index of the month
        """
        return str(self.month).zfill(2)
