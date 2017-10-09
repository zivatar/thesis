import unittest
import datetime
from .climate import Climate

class ClimateTestCase(unittest.TestCase):

	'''
	Frost days: Tmin < 0
	'''
	def test_frost_days(self):
		self.assertEqual(Climate.getNrFrostDays([0.0, 0.1, 0.5, 11.0, 111.1]), 0)
		self.assertEqual(Climate.getNrFrostDays([]), 0)
		self.assertEqual(Climate.getNrFrostDays([0.0, -0.1, 0.0]), 1)
		self.assertEqual(Climate.getNrFrostDays([0.0, 0.0, 0.0]), 0)
		self.assertEqual(Climate.getNrFrostDays([-1.1, -2.2, -3.3, -99.9]), 4)

	'''
	Cold days: Tmin < 10
	'''
	def test_cold_days(self):
		self.assertEqual(Climate.getNrColdDays([2.5, 0.0, 9.9, -9.9]), 0)
		self.assertEqual(Climate.getNrColdDays([]), 0)
		self.assertEqual(Climate.getNrColdDays([-10.0, -9.9, 9.9, -10.1]), 1)

if __name__ == '__main__':
	unittest.main()