import unittest

from climate.classes.Year import Year

if __name__ == '__main__':
    unittest.main()


class YearTestCase(unittest.TestCase):

    def test_get_month(self):
        self.assertEqual(Year.get_months_of_year(), list(range(1, 13)))


