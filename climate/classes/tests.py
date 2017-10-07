import unittest
from .weather import Weather

class WeatherTestCase(unittest.TestCase):

	'''
	Constants should exist and have valid values
	'''
	def test_class_init(self):
		self.assertEqual(Weather.WEATHER_CODE[0], (1, 'füst'))
		self.assertEqual(Weather.BEAUFORT_SCALE[0], (-1, 'nem észlelt'))

	'''
	Transform weather code to its name
	'''
	def test_valid_code(self):
		self.assertEqual(Weather.getWeatherCodeText(1), 'füst')
	def test_invalid_code(self):
		self.assertEqual(Weather.getWeatherCodeText(9999), None)
	def test_empty_code(self):
		self.assertEqual(Weather.getWeatherCodeText(), None)

if __name__ == '__main__':
	unittest.main()