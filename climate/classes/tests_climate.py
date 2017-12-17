import unittest
import datetime
from .climate import Climate

class ClimateTestCase(unittest.TestCase):

	'''
	Frost days: Tmin < 0
	'''
	def test_frost_days_positive(self):
		self.assertEqual(Climate.getNrFrostDays([0.0, 0.1, 0.5, 11.0, 111.1]), 0)

	def test_frost_days_empty(self):
		self.assertEqual(Climate.getNrFrostDays([]), 0)

	def test_frost_days_around(self):
		self.assertEqual(Climate.getNrFrostDays([0.0, -0.1, 0.0]), 1)

	def test_frost_days_zero(self):
		self.assertEqual(Climate.getNrFrostDays([0.0, 0.0, 0.0]), 0)

	def test_frost_days_negative(self):
		self.assertEqual(Climate.getNrFrostDays([-1.1, -2.2, -3.3, -99.9]), 4)

	def test_frost_days_only_null(self):
		self.assertEqual(Climate.getNrFrostDays([None, None, None]), 0)

	def test_frost_days_with_null(self):
		self.assertEqual(Climate.getNrFrostDays([-0.1, None, 0.1]), 1)


	'''
	Cold days: Tmin < -10
	'''
	def test_cold_days(self):
		self.assertEqual(Climate.getNrColdDays([2.5, 0.0, 9.9, -9.9]), 0)

	def test_cold_days_empty(self):
		self.assertEqual(Climate.getNrColdDays([]), 0)

	def test_cold_days_around(self):
		self.assertEqual(Climate.getNrColdDays([-10.0, -9.9, 9.9, -10.1]), 1)

	def test_cold_days_below(self):
		self.assertEqual(Climate.getNrColdDays([-10.1, -14.4, -99.9]), 3)

	def test_cold_days_with_null(self):
		self.assertEqual(Climate.getNrColdDays([-9.9, None, -10.1]), 1)

	def test_cold_days_only_null(self):
		self.assertEqual(Climate.getNrColdDays([None, None, None]), 0)


	'''
	Warm nights: Tmin > 20
	'''
	def test_warm_nights_empty(self):
		self.assertEqual(Climate.getNrWarmNights([]), 0)

	def test_warm_nights_below(self):
		self.assertEqual(Climate.getNrWarmNights([-5, 0, 5, 10]), 0)

	def test_warm_nights_above(self):
		self.assertEqual(Climate.getNrWarmNights([20.1, 25]), 2)

	def test_warm_nights(self):
		self.assertEqual(Climate.getNrWarmNights([10, 30]), 1)

	def test_warm_nights_with_null(self):
		self.assertEqual(Climate.getNrWarmNights([None, 21]), 1)

	def test_warm_nights_only_null(self):
		self.assertEqual(Climate.getNrWarmNights([None, None, None]), 0)


	'''
	Summer days: Tmax > 25
	'''
	def test_summer_days_empty(self):
		self.assertEqual(Climate.getNrSummerDays([]),0)

	def test_summer_days_below(self):
		self.assertEqual(Climate.getNrSummerDays([-5, 0, 10]), 0)

	def test_summer_days_above(self):
		self.assertEqual(Climate.getNrSummerDays([25.1, 30]), 2)

	def test_summer_days_around(self):
		self.assertEqual(Climate.getNrSummerDays([24.9, 25.0, 25.1]), 1)

	def test_summer_days_only_null(self):
		self.assertEqual(Climate.getNrSummerDays([None, None]), 0)

	def test_summer_days_with_null(self):
		self.assertEqual(Climate.getNrSummerDays([None, 24, 26]), 1)


	'''
	Warm days: Tmax >= 30
	'''
	def test_warm_days_empty(self):
		self.assertEqual(Climate.getNrWarmDays([]), 0)

	def test_warm_days_below(self):
		self.assertEqual(Climate.getNrWarmDays([-10, 0, 29.9]), 0)

	def test_warm_days_above(self):
		self.assertEqual(Climate.getNrWarmDays([30.0, 30.1, 45]), 3)

	def test_warm_days_around(self):
		self.assertEqual(Climate.getNrWarmDays([29.9, 30.0, 30.1]), 2)

	def test_warm_days_with_null(self):
		self.assertEqual(Climate.getNrWarmDays([29.9, None, 30.0]), 1)

	def test_warm_days_only_null(self):
		self.assertEqual(Climate.getNrWarmDays([None, None]), 0)


	'''
	Hot days: Tmax >= 35
	'''
	def test_hot_days_empty(self):
		self.assertEqual(Climate.getNrHotDays([]), 0)

	def test_hot_days_below(self):
		self.assertEqual(Climate.getNrHotDays([-4, 4, 34.9]), 0)

	def test_hot_days_above(self):
		self.assertEqual(Climate.getNrHotDays([35.0, 35.1, 40]), 3)

	def test_hot_days_around(self):
		self.assertEqual(Climate.getNrHotDays([34.9, 35.0]), 1)

	def test_hot_days_with_null(self):
		self.assertEqual(Climate.getNrHotDays([34.9, None, 35.0]), 1)

	def test_hot_days_only_null(self):
		self.assertEqual(Climate.getNrHotDays([None, None]), 0)


	'''
	Precipitation limit reaches
	'''
	def test_prec_dist_empty(self):
		self.assertEqual(Climate.getPrecDistribution([]), {0: 0, 10: 0, 30: 0, 50: 0})

	def test_prec_dist_zero(self):
		self.assertEqual(Climate.getPrecDistribution([0, 0, 0]), {0: 0, 10: 0, 30: 0, 50: 0})

	def test_prec_small(self):
		self.assertEqual(Climate.getPrecDistribution([0, 0.1, 0.5, 1]), {0: 3, 10: 0, 30: 0, 50: 0})

	def test_prec_med(self):
		self.assertEqual(Climate.getPrecDistribution([0, 0.1, 10.0, 10.1]), {0: 3, 10: 2, 30: 0, 50: 0})

	def test_prec_high(self):
		self.assertEqual(Climate.getPrecDistribution([0, 0.1, 10.0, 50.0, 150]), {0: 4, 10: 3, 30: 2, 50: 2})


	'''
	Sum of not none elements
	'''
	def test_sum_empty(self):
		self.assertEqual(Climate.sum([]), 0)

	def test_sum_only_null(self):
		self.assertEqual(Climate.sum([None, None]), 0)

	def test_sum_with_null(self):
		self.assertEqual(Climate.sum([0, 5, None, -1]), 4)

	def test_sum_without_null(self):
		self.assertEqual(Climate.sum([0, 2, -4]), -2)


	'''
	Number of not none elements
	'''
	def test_num_empty(self):
		self.assertEqual(Climate.number([]), 0)

	def test_num_only_null(self):
		self.assertEqual(Climate.number([None, None]), 0)

	def test_num_with_null(self):
		self.assertEqual(Climate.number([None, 2.1, "abc", -11]), 3)


	'''
	Number of not none elements in list2
	'''
	def test_num2_empty(self):
		self.assertEqual(Climate.number2([]), 0)

	def test_num2_empty2(self):
		self.assertEqual(Climate.number2([[],[]]), 0)

	def test_num2_only_none(self):
		self.assertEqual(Climate.number2([[None], [None]]), 0)

	def test_num2_with_none(self):
		self.assertEqual(Climate.number2([[0, 1, None], [2, None]]), 3)

	def test_num2_not_none(self):
		self.assertEqual(Climate.number2([[-5, 10, 0], [1, 3, 4]]), 6)

	def test_num2_empty_strict(self):
		self.assertEqual(Climate.number2([], strict=True), 0)

	def test_num2_empty2_strict(self):
		self.assertEqual(Climate.number2([[],[]], strict=True), 0)

	def test_num2_only_none_strict(self):
		self.assertEqual(Climate.number2([[None], [None]], strict=True), 0)

	def test_num2_with_none_strict(self):
		self.assertEqual(Climate.number2([[0, 1, None], [2, None]], strict=True), 2)

	def test_num2_not_none_strict(self):
		self.assertEqual(Climate.number2([[-5, 10, 0], [1, 3, 4]], strict=True), 5)



if __name__ == '__main__':
	unittest.main()