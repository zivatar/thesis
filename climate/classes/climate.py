from .weather import Weather


class Climate(object):
    TEMP_DISTRIBUTION_LIMITS = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
    RH_DISTRIBUTION_LIMITS = [20, 40, 60, 80]
    WIND_DIRECTION_LIMITS = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]

    # input list of Tmins or list of Tmaxs
    @staticmethod
    def get_nr_frost_days(min_temperature_list):
        return len([x for x in min_temperature_list if x is not None and x < 0])

    @staticmethod
    def get_nr_winter_days(max_temperature_list):
        return len([x for x in max_temperature_list if x is not None and x <= 0])

    @staticmethod
    def get_nr_cold_days(min_temperature_list):
        return len([x for x in min_temperature_list if x is not None and x < -10])

    @staticmethod
    def get_nr_warm_nights(min_temperature_list):
        return len([x for x in min_temperature_list if x is not None and x > 20])

    @staticmethod
    def get_nr_summer_days(max_temperature_list):
        return len([x for x in max_temperature_list if x is not None and x > 25])

    @staticmethod
    def get_nr_warm_days(max_temperature_list):
        return len([x for x in max_temperature_list if x is not None and x >= 30])

    @staticmethod
    def get_nr_hot_days(max_temperature_list):
        return len([x for x in max_temperature_list if x is not None and x >= 35])

    @staticmethod
    def get_precipitation_over_limits(daily_precipitation_list):
        d0 = len([j for j in daily_precipitation_list if j is not None and j > 0])
        d10 = len([j for j in daily_precipitation_list if j is not None and j >= 10])
        d30 = len([j for j in daily_precipitation_list if j is not None and j >= 30])
        d50 = len([j for j in daily_precipitation_list if j is not None and j >= 50])
        return {0: d0, 10: d10, 30: d30, 50: d50}

    @staticmethod
    def sum(input_list):
        summary = 0.0
        for i in input_list:
            if i is not None:
                summary = summary + float(i)
        return summary

    @staticmethod
    def number(input_list):
        num = 0
        for i in input_list:
            if i is not None:
                num = num + 1
        return num

    @staticmethod
    def number2(input_list, strict=False):
        num = 0
        for i in input_list:
            for j in i:
                if j is not None and (not strict or j != 0):
                    num = num + 1
        return num

    @staticmethod
    def avg(input_list):
        summary = 0.0
        num = 0
        for i in input_list:
            if i is not None:
                summary = summary + float(i)
                num = num + 1
        if num == 0:
            return None
        return summary / num

    @staticmethod
    def avg2(list1, list2):
        if len(list1) != len(list2):
            return None
        summary = 0.0
        num = 0
        for i in zip(list1, list2):
            if i[0] is not None and i[1] is not None:
                summary = summary + float(i[0]) + float(i[1])
                num = num + 2
        if num == 0:
            return None
        return summary / num

    @staticmethod
    def calculate_distribution(data, limits):
        res = []
        for i in range(len(limits)):
            low = None
            high = None
            if i == 0:
                high = limits[i]
            elif i == len(limits) - 1:
                low = limits[i]
            else:
                low = limits[i]
                high = limits[i + 1]
            sublist = [x for x in data if x is not None and (high is None or x <= high) and (low is None or x > low)]
            res.append(len(sublist))
        return res

    @staticmethod
    def calculate_temperature_distribution(temps):
        data = Climate.calculate_distribution(temps, Climate.TEMP_DISTRIBUTION_LIMITS)
        return data

    @staticmethod
    def calculate_rh_distribution(rhs):
        data = Climate.calculate_distribution(rhs, Climate.RH_DISTRIBUTION_LIMITS)
        return data

    @staticmethod
    def calculate_wind_distribution(rhs):
        data = Climate.calculate_distribution(rhs, Climate.WIND_DIRECTION_LIMITS)
        return data

    @staticmethod
    def count_significants(significant, daily):
        for code in Weather.WEATHER_CODE:
            number = significant.get(code[0], 0)
            if str(code[0]) in daily:
                number = number + 1
            significant[code[0]] = number
        return significant
