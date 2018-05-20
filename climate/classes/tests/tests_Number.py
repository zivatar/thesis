import unittest

from climate.classes.Number import Number

if __name__ == '__main__':
    unittest.main()


class TestNumber(unittest.TestCase):
    parametrize = [
        ('', False, None, None),
        (' ', False, None, None),
        ('nkfdkd', False, None, None),
        ('kfjkd883kfdj39u39', False, None, None),
        ('1', True, 1.0, 1),
        ('-3.1415', True, -3.1415, None),
        ('050.050', True, 50.05, None),
        ('999999999999', True, 999999999999.0, 999999999999)
    ]

    def test_is_number(self):
        for p in TestNumber.parametrize:
            with self.subTest():
                self.assertEqual(Number.is_number(p[0]), p[1])

    def test_to_float(self):
        for p in TestNumber.parametrize:
            with self.subTest():
                self.assertEqual(Number.to_float(p[0]), p[2])

    def test_to_int(self):
        for p in TestNumber.parametrize:
            with self.subTest():
                self.assertEqual(Number.to_int(p[0]), p[3])
