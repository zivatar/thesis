import unittest

from climate.classes.Report import Report

if __name__ == '__main__':
    unittest.main()


class ReportTestCase(unittest.TestCase):
    class WithoutSnow:
        isSnow = False

    class WithSnow:
        isSnow = True

    def test_empty(self):
        r = Report()
        self.assertEqual(r.get_nr_of_snow_days(), 0)

    def test_zero_snow(self):
        r = Report()
        r.manualDayObjs = [self.WithoutSnow(), self.WithoutSnow(), self.WithoutSnow()]
        self.assertEqual(r.get_nr_of_snow_days(), 0)

    def test_some_snow(self):
        r = Report()
        r.manualDayObjs = [self.WithoutSnow(), self.WithSnow(), self.WithoutSnow(), self.WithSnow()]
        self.assertEqual(r.get_nr_of_snow_days(), 2)

    def test_all_snow(self):
        r = Report()
        r.manualDayObjs = [self.WithSnow(), self.WithSnow(), self.WithSnow()]
        self.assertEqual(r.get_nr_of_snow_days(), 3)
