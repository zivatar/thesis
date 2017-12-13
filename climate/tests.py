from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        TestCases are running well
        """
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()