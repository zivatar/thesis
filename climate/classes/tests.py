import unittest
from .weather import Weather

class WeatherTestCase(unittest.TestCase):
	'''
	Constants should exist and have valid values
	'''
	def test_class_init(self):
		self.assertEqual(Weather.WEATHER_CODE[0], (1, 'füst'))
		self.assertEqual(Weather.BEAUFORT_SCALE[0], (-1, 'nem észlelt'))
	def test_valid_text(self):
		self.assertEqual(Weather.getWeatherCodeText(1), 'füst')

if __name__ == '__main__':
	unittest.main()