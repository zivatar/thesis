import unittest
from datetime import datetime

from django.utils import timezone

from climate.classes.Month import Month


class MonthTestCase(unittest.TestCase):

    # Init and get month, day

    def test_init_get_valid(self):
        month = Month()
        now = timezone.now()
        self.assertEqual(month.get_date_readable(), str(now.year) + "." + str(now.month) + ".")
        self.assertEqual(month.get_month_two_digits(), str(now.month).zfill(2))

    def test_init_numbers(self):
        month = Month(year=2017, month=8)
        self.assertEqual(month.get_date_readable(), str(2017) + "." + str(8) + ".")
        self.assertEqual(month.get_month_two_digits(), '08')

    def test_init_strings(self):
        month = Month(year="2017", month="08")
        self.assertEqual(month.get_date_readable(), str(2017) + "." + str(8) + ".")
        self.assertEqual(month.get_month_two_digits(), '08')

    def test_init_invalid_values(self):
        month = Month(year=0, month=0)
        now = timezone.now()
        self.assertEqual(month.get_date_readable(), str(now.year) + "." + str(now.month) + ".")
        self.assertEqual(month.get_month_two_digits(), str(now.month).zfill(2))

    # Date is in month

    def test_date_is_in_month(self):
        month = Month(year=2017, month=10)
        test_date = datetime.date(2017, 10, 11)
        self.assertTrue(month.is_in_month(test_date))

    def test_bad_month(self):
        month = Month(year=2017, month=10)
        test_date = datetime.date(2017, 12, 11)
        self.assertFalse(month.is_in_month(test_date))

    def test_bad_year(self):
        month = Month(year=2017, month=10)
        test_date = datetime.date(2016, 10, 11)
        self.assertFalse(month.is_in_month(test_date))

    # Return days of month in array

    def test_days_of_jan(self):
        month = Month(year=2017, month=1)
        self.assertEqual(month.days_of_month(), list(range(1, 32)))

    def test_days_of_feb_leaping(self):
        month = Month(year=2016, month=2)
        self.assertEqual(month.days_of_month(), list(range(1, 30)))

    def test_days_of_feb_non_leaping(self):
        month = Month(year=2017, month=2)
        self.assertEqual(month.days_of_month(), list(range(1, 29)))

    # Return past days of current month in array

    def test_days_of_month_till_today(self):
        today = timezone.now().day
        self.assertEqual(Month().days_of_month_till_today(), list(range(1, today + 1)))

    def test_days_of_month_till_other_day(self):
        other_day = Month(year=2017, month=1)
        self.assertEqual(other_day.days_of_month_till_today(), list(range(1, 32)))

    # Next, prev


if __name__ == '__main__':
    unittest.main()
