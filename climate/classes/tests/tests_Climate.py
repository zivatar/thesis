import unittest

from random import random

from climate.classes.Climate import Climate
from climate.classes.Weather import Weather


class FrostDays(unittest.TestCase):
    """
    Frost days: Tmin < 0 C
    """

    def test_frost_days_positive(self):
        self.assertEqual(Climate.get_nr_frost_days([0.0, 0.1, 0.5, 11.0, 111.1]), 0)

    def test_frost_days_empty(self):
        self.assertEqual(Climate.get_nr_frost_days([]), 0)

    def test_frost_days_around(self):
        self.assertEqual(Climate.get_nr_frost_days([0.0, -0.1, 0.0]), 1)

    def test_frost_days_zero(self):
        self.assertEqual(Climate.get_nr_frost_days([0.0, 0.0, 0.0]), 0)

    def test_frost_days_negative(self):
        self.assertEqual(Climate.get_nr_frost_days([-1.1, -2.2, -3.3, -99.9]), 4)

    def test_frost_days_only_null(self):
        self.assertEqual(Climate.get_nr_frost_days([None, None, None]), 0)

    def test_frost_days_with_null(self):
        self.assertEqual(Climate.get_nr_frost_days([-0.1, None, 0.1]), 1)


class ColdDays(unittest.TestCase):
    """
    Cold days: Tmin < -10 C
    """

    def test_cold_days(self):
        self.assertEqual(Climate.get_nr_cold_days([2.5, 0.0, 9.9, -9.9]), 0)

    def test_cold_days_empty(self):
        self.assertEqual(Climate.get_nr_cold_days([]), 0)

    def test_cold_days_around(self):
        self.assertEqual(Climate.get_nr_cold_days([-10.0, -9.9, 9.9, -10.1]), 1)

    def test_cold_days_below(self):
        self.assertEqual(Climate.get_nr_cold_days([-10.1, -14.4, -99.9]), 3)

    def test_cold_days_with_null(self):
        self.assertEqual(Climate.get_nr_cold_days([-9.9, None, -10.1]), 1)

    def test_cold_days_only_null(self):
        self.assertEqual(Climate.get_nr_cold_days([None, None, None]), 0)


class WarmNights(unittest.TestCase):
    """
    Warm nights: Tmin > 20 C
    """

    def test_warm_nights_empty(self):
        self.assertEqual(Climate.get_nr_warm_nights([]), 0)

    def test_warm_nights_below(self):
        self.assertEqual(Climate.get_nr_warm_nights([-5, 0, 5, 10]), 0)

    def test_warm_nights_above(self):
        self.assertEqual(Climate.get_nr_warm_nights([20.1, 25]), 2)

    def test_warm_nights(self):
        self.assertEqual(Climate.get_nr_warm_nights([10, 30]), 1)

    def test_warm_nights_with_null(self):
        self.assertEqual(Climate.get_nr_warm_nights([None, 21]), 1)

    def test_warm_nights_only_null(self):
        self.assertEqual(Climate.get_nr_warm_nights([None, None, None]), 0)


class SummerDays(unittest.TestCase):
    """
    Summer days: Tmax > 25 C
    """

    def test_summer_days_empty(self):
        self.assertEqual(Climate.get_nr_summer_days([]), 0)

    def test_summer_days_below(self):
        self.assertEqual(Climate.get_nr_summer_days([-5, 0, 10]), 0)

    def test_summer_days_above(self):
        self.assertEqual(Climate.get_nr_summer_days([25.1, 30]), 2)

    def test_summer_days_around(self):
        self.assertEqual(Climate.get_nr_summer_days([24.9, 25.0, 25.1]), 1)

    def test_summer_days_only_null(self):
        self.assertEqual(Climate.get_nr_summer_days([None, None]), 0)

    def test_summer_days_with_null(self):
        self.assertEqual(Climate.get_nr_summer_days([None, 24, 26]), 1)


class WarmDays(unittest.TestCase):
    """
    Warm days: Tmax >= 30 C
    """

    def test_warm_days_empty(self):
        self.assertEqual(Climate.get_nr_warm_days([]), 0)

    def test_warm_days_below(self):
        self.assertEqual(Climate.get_nr_warm_days([-10, 0, 29.9]), 0)

    def test_warm_days_above(self):
        self.assertEqual(Climate.get_nr_warm_days([30.0, 30.1, 45]), 3)

    def test_warm_days_around(self):
        self.assertEqual(Climate.get_nr_warm_days([29.9, 30.0, 30.1]), 2)

    def test_warm_days_with_null(self):
        self.assertEqual(Climate.get_nr_warm_days([29.9, None, 30.0]), 1)

    def test_warm_days_only_null(self):
        self.assertEqual(Climate.get_nr_warm_days([None, None]), 0)


class HotDays(unittest.TestCase):
    """
    Hot days: Tmax >= 35 C
    """

    def test_hot_days_empty(self):
        self.assertEqual(Climate.get_nr_hot_days([]), 0)

    def test_hot_days_below(self):
        self.assertEqual(Climate.get_nr_hot_days([-4, 4, 34.9]), 0)

    def test_hot_days_above(self):
        self.assertEqual(Climate.get_nr_hot_days([35.0, 35.1, 40]), 3)

    def test_hot_days_around(self):
        self.assertEqual(Climate.get_nr_hot_days([34.9, 35.0]), 1)

    def test_hot_days_with_null(self):
        self.assertEqual(Climate.get_nr_hot_days([34.9, None, 35.0]), 1)

    def test_hot_days_only_null(self):
        self.assertEqual(Climate.get_nr_hot_days([None, None]), 0)


class WinterDays(unittest.TestCase):
    """
    Winter days: Tmax <= 0 C
    """

    def test_winter_days_only_null(self):
        self.assertEqual(Climate.get_nr_winter_days([None, None]), 0)

    def test_winter_days_with_null(self):
        self.assertEqual(Climate.get_nr_winter_days([None, 1, 2]), 0)

    def test_winter_days_empty(self):
        self.assertEqual(Climate.get_nr_winter_days([]), 0)

    def test_winter_days_above(self):
        self.assertEqual(Climate.get_nr_winter_days([0.1, 3, 99]), 0)

    def test_winter_days_below(self):
        self.assertEqual(Climate.get_nr_winter_days([-0.1, -10, -99]), 3)

    def test_winter_days_around(self):
        self.assertEqual(Climate.get_nr_winter_days([-0.1, 0, 0.1]), 2)


class PrecipitationLimits(unittest.TestCase):

    def test_prec_dist_empty(self):
        self.assertEqual(Climate.get_precipitation_over_limits([]), {0: 0, 10: 0, 30: 0, 50: 0})

    def test_prec_dist_zero(self):
        self.assertEqual(Climate.get_precipitation_over_limits([0, 0, 0]), {0: 0, 10: 0, 30: 0, 50: 0})

    def test_prec_small(self):
        self.assertEqual(Climate.get_precipitation_over_limits([0, 0.1, 0.5, 1]), {0: 3, 10: 0, 30: 0, 50: 0})

    def test_prec_med(self):
        self.assertEqual(Climate.get_precipitation_over_limits([0, 0.1, 10.0, 10.1]), {0: 3, 10: 2, 30: 0, 50: 0})

    def test_prec_high(self):
        self.assertEqual(Climate.get_precipitation_over_limits([0, 0.1, 10.0, 50.0, 150]), {0: 4, 10: 3, 30: 2, 50: 2})


class Summarize(unittest.TestCase):
    """
    Summarize not none elements in list
    """

    def test_sum_empty(self):
        self.assertEqual(Climate.sum([]), 0)

    def test_sum_only_null(self):
        self.assertEqual(Climate.sum([None, None]), 0)

    def test_sum_with_null(self):
        self.assertEqual(Climate.sum([0, 5, None, -1]), 4)

    def test_sum_without_null(self):
        self.assertEqual(Climate.sum([0, 2, -4]), -2)


class NumberOfElementsInList(unittest.TestCase):
    """
    Number of not none elements in list
    """

    def test_num_empty(self):
        self.assertEqual(Climate.number([]), 0)

    def test_num_only_null(self):
        self.assertEqual(Climate.number([None, None]), 0)

    def test_num_with_null(self):
        self.assertEqual(Climate.number([None, 2.1, "abc", -11]), 3)


class NumberOfElementsInList2(unittest.TestCase):
    """
    Number of not none elements in list2
    """

    def test_num2_empty(self):
        self.assertEqual(Climate.number2([]), 0)

    def test_num2_empty2(self):
        self.assertEqual(Climate.number2([[], []]), 0)

    def test_num2_only_none(self):
        self.assertEqual(Climate.number2([[None], [None]]), 0)

    def test_num2_with_none(self):
        self.assertEqual(Climate.number2([[0, 1, None], [2, None]]), 3)

    def test_num2_not_none(self):
        self.assertEqual(Climate.number2([[-5, 10, 0], [1, 3, 4]]), 6)

    def test_num2_empty_strict(self):
        self.assertEqual(Climate.number2([], strict=True), 0)

    def test_num2_empty2_strict(self):
        self.assertEqual(Climate.number2([[], []], strict=True), 0)

    def test_num2_only_none_strict(self):
        self.assertEqual(Climate.number2([[None], [None]], strict=True), 0)

    def test_num2_with_none_strict(self):
        self.assertEqual(Climate.number2([[0, 1, None], [2, None]], strict=True), 2)

    def test_num2_not_none_strict(self):
        self.assertEqual(Climate.number2([[-5, 10, 0], [1, 3, 4]], strict=True), 5)


class AverageElementsInList(unittest.TestCase):
    def test_avg_empty(self):
        self.assertEqual(Climate.avg([]), None)

    def test_avg_with_none(self):
        self.assertEqual(Climate.avg([-2, None, -1]), -1.5)

    def test_avg_only_none(self):
        self.assertEqual(Climate.avg([None, None, None]), None)

    def test_avg_not_none(self):
        self.assertEqual(Climate.avg([0, 5, 10]), 5)


class AverageElementsInList2(unittest.TestCase):
    def test_avg2_empty(self):
        self.assertEqual(Climate.avg2([], []), None)

    def test_avg2_half_empty(self):
        self.assertEqual(Climate.avg2([], [1, 2, 3]), None)

    def test_avg2_different_length(self):
        self.assertEqual(Climate.avg2([1, 2, 3], [1, 2]), None)


class ClimateConstants(unittest.TestCase):
    def test_TEMP_DISTRIBUTION_LIMITS(self):
        self.assertEqual(Climate.TEMP_DISTRIBUTION_LIMITS,
                         [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40])

    def test_RH_DSTRIBUTION_LIMITS(self):
        self.assertEqual(Climate.RH_DISTRIBUTION_LIMITS, [20, 40, 60, 80])

    def test_WIND_DIRECTION_LIMITS(self):
        self.assertEqual(Climate.WIND_DIRECTION_LIMITS,
                         [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5])


class Distributions(unittest.TestCase):
    def test_empty_data(self):
        self.assertEqual(Climate.calculate_distribution(data=[], limits=[0, 1, 2]), [0, 0, 0])

    def test_none_data(self):
        self.assertEqual(Climate.calculate_distribution(data=None, limits=[0, 1, 2]), None)

    def test_empty_limits(self):
        self.assertEqual(Climate.calculate_distribution(data=[1, 2, 3], limits=[]), [])

    def test_none_limits(self):
        self.assertEqual(Climate.calculate_distribution(data=[1, 2, 3], limits=None), None)

    def test_below_limit(self):
        self.assertEqual(Climate.calculate_distribution(data=[-1, -2], limits=[0, 1, 2]), [2, 0, 0])

    def test_above_limit(self):
        self.assertEqual(Climate.calculate_distribution(data=[4, 5], limits=[0, 1, 2]), [0, 0, 2])

    def test_between_limits(self):
        self.assertEqual(Climate.calculate_distribution(data=[1.1, 2.0], limits=[0, 1, 2]), [0, 2, 0])


class TemperatureDistributions(unittest.TestCase):
    data = [(random() - 0.5) * 40 for i in range(10)]
    params = [[], None, data]

    def test_temperature_distribution(self):
        for p in self.params:
            with self.subTest():
                self.assertEqual(Climate.calculate_temperature_distribution(temps=p),
                                 Climate.calculate_distribution(data=p,
                                                                limits=Climate.TEMP_DISTRIBUTION_LIMITS))


class RelativeHumidityDistributions(unittest.TestCase):
    data = [random() * 100 for i in range(10)]
    params = [[], None, data]

    def test_rh_distribution(self):
        for p in self.params:
            with self.subTest():
                self.assertEqual(Climate.calculate_rh_distribution(rhs=p),
                                 Climate.calculate_distribution(data=p,
                                                                limits=Climate.RH_DISTRIBUTION_LIMITS))


class WindDirectionDistributions(unittest.TestCase):
    data = [random() * 360 for i in range(10)]
    params = [[], None, data]

    def test_wind_distribution(self):
        for p in self.params:
            with self.subTest():
                self.assertEqual(Climate.calculate_wind_distribution(rhs=p),
                                 Climate.calculate_distribution(data=p,
                                                                limits=Climate.WIND_DIRECTION_LIMITS))


class CountSignificants(unittest.TestCase):
    parametrize = [
        (['4', '19'], {4: 1, 19: 1}),
        (['1', '1'], {1: 1}),
        (['1', '100', '99'], {1: 1, 100: 1, 99: 1}),
        ([], {}),
        (None, {})
    ]

    def test_valid(self):
        for p in self.parametrize:
            with self.subTest():
                significant = Climate.count_significants(significant={}, daily=p[0])
                for k in significant.keys():
                    expected_value = p[1].get(k, 0)
                    self.assertEqual(significant[k], expected_value)
                    self.assertIsNotNone(Weather.get_weather_code_text(k))


if __name__ == '__main__':
    unittest.main()
