from django.utils import timezone
import calendar


class Month:
    def __init__(self, now=timezone.now(), year=0, month=0):
        if year == 0 or month == 0:
            self.year = now.year
            self.month = now.month
            self._currentMonth = True
        else:
            self.year = int(year)
            self.month = int(month)
            self._currentMonth = False

    def get_date_readable(self):
        return str(self.year) + "." + str(self.month) + "."

    def is_in_month(self, dt):
        return self.year == dt.year and self.month == dt.month

    def last_day(self):
        return calendar.monthrange(self.year, self.month)[1]

    def days_of_month(self):
        last_day = calendar.monthrange(self.year, self.month)[1]
        a = []
        [a.append(i) for i in range(1, last_day + 1)]
        return a

    def days_of_month_till_today(self):
        if self._currentMonth:
            last_day = timezone.now().day
        else:
            last_day = calendar.monthrange(self.year, self.month)[1]
        a = []
        [a.append(i) for i in range(1, last_day + 1)]
        return a

    def get_month_two_digits(self):
        return str(self.month).zfill(2)
