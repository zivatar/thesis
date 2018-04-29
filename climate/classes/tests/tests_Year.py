import unittest

from climate.classes.Year import Year


class YearTestCase(unittest.TestCase):

    # getMonth

    def test_get_month(self):
        self.assertEqual(Year.months_of_year(), list(range(1, 13)))


if __name__ == '__main__':
    unittest.main()
