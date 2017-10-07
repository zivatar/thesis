from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        TestCases are running well
        """
        self.assertEqual(1 + 1, 2)

from .utils import gravatar as gr
class GravatarTestCase(TestCase):
	def test_empty_email(self):
		self.assertEqual(gr.gravatar_url(''), 'https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?d=identicon&s=100')
	def test_real_email_without_gravatar(self):
		self.assertEqual(gr.gravatar_url('rendeles10@gmail.com'), 'https://www.gravatar.com/avatar/63f5e37aadce48600a133c88d4b89fe8?d=identicon&s=100')
	def test_real_email_with_gravatar(self):
		self.assertEqual(gr.gravatar_url('macgyver1024@gmail.com'), 'https://www.gravatar.com/avatar/58c594b1465ea0c8d93c8860dfb16a30?d=identicon&s=100')
	def test_xl_size(self):
		self.assertEqual(gr.gravatar_url('rendeles10@gmail.com', 512), 'https://www.gravatar.com/avatar/63f5e37aadce48600a133c88d4b89fe8?d=identicon&s=512')

from .classes.weather import Weather
class WeatherTestCase(TestCase):
	def test_constants(self):
		pass

if __name__ == '__main__':
    unittest.main()