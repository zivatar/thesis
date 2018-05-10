from climate.classes.Weather import Weather


class Climate(object):
    """
    | Calculations with climate based business logic
    """
    TEMP_DISTRIBUTION_LIMITS = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
    RH_DISTRIBUTION_LIMITS = [20, 40, 60, 80]
    WIND_DIRECTION_LIMITS = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]

    @staticmethod
    def get_nr_frost_days(min_temperature_list):
        """
        Calculate number of frost days

        :param min_temperature_list: daily minimum temperature values in Celsius
        :type min_temperature_list: list of numbers
        :return: number of days
        """
        return len([x for x in min_temperature_list if x is not None and x < 0])

    @staticmethod
    def get_nr_winter_days(max_temperature_list):
        """
        Calculate number of winter days

        :param max_temperature_list: daily maximum temperature values in Celsius
        :type max_temperature_list: list of numbers
        :return: number of days
        """
        return len([x for x in max_temperature_list if x is not None and x <= 0])

    @staticmethod
    def get_nr_cold_days(min_temperature_list):
        """
        Calculate number of cold days

        :param min_temperature_list: daily minimum temperature values in Celsius
        :type min_temperature_list: list of numbers
        :return: number of days
        """
        return len([x for x in min_temperature_list if x is not None and x < -10])

    @staticmethod
    def get_nr_warm_nights(min_temperature_list):
        """
        Calculate number of warm nights

        :param min_temperature_list: daily minimum temperature values in Celsius
        :type min_temperature_list: list of numbers
        :return: number of days
        """
        return len([x for x in min_temperature_list if x is not None and x > 20])

    @staticmethod
    def get_nr_summer_days(max_temperature_list):
        """
        Calculate number of summer days

        :param max_temperature_list: daily maximum temperature values in Celsius
        :type max_temperature_list: list of numbers
        :return: number of days
        """
        return len([x for x in max_temperature_list if x is not None and x > 25])

    @staticmethod
    def get_nr_warm_days(max_temperature_list):
        """
        Calculate number of warm days

        :param max_temperature_list: daily maximum temperature values in Celsius
        :type max_temperature_list: list of numbers
        :return: number of days
        """
        return len([x for x in max_temperature_list if x is not None and x >= 30])

    @staticmethod
    def get_nr_hot_days(max_temperature_list):
        """
        Calculate number of hot days

        :param max_temperature_list: daily maxiumum temperature values in Celsius
        :type max_temperature_list: list of numbers
        :return: number of days
        """
        return len([x for x in max_temperature_list if x is not None and x >= 35])

    @staticmethod
    def get_precipitation_over_limits(daily_precipitation_list):
        """
        Calculate number of days exceeding important precipitation amount limits

        :param daily_precipitation_list: daily precipitation amount in mm
        :type daily_precipitation_list: list of numbers
        :return: number of days in a dictionary {0: d0, 10: d10, 30: d30, 50: d50}
        """
        d0 = len([j for j in daily_precipitation_list if j is not None and j > 0])
        d10 = len([j for j in daily_precipitation_list if j is not None and j >= 10])
        d30 = len([j for j in daily_precipitation_list if j is not None and j >= 30])
        d50 = len([j for j in daily_precipitation_list if j is not None and j >= 50])
        return {0: d0, 10: d10, 30: d30, 50: d50}

    @staticmethod
    def sum(input_list):
        """
        Summarize the elements of a list

        :param input_list: numbers
        :type input_list: list
        :return: summary
        """
        summary = 0.0
        for i in input_list:
            if i is not None:
                summary = summary + float(i)
        return summary

    @staticmethod
    def number(input_list):
        """
        Count not None elements of a list

        :param input_list: numbers
        :type input_list: list
        :return: count of elements
        """
        num = 0
        for i in input_list:
            if i is not None:
                num = num + 1
        return num

    @staticmethod
    def number2(input_list, strict=False):
        """
        Count not None elements of a list containing lists

        :param input_list: numbers
        :type input_list: list of list
        :param strict: if zero number does not count
        :type strict: boolean
        :return: count of elements
        """
        num = 0
        for i in input_list:
            for j in i:
                if j is not None and (not strict or j != 0):
                    num = num + 1
        return num

    @staticmethod
    def avg(input_list):
        """
        Calculate the average of the not None elements of a list

        :param input_list:
        :type input_list: list of numbers
        :return: average value
        """
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
        """
        Calculate average of two lists where neither of the adjacent elements is None

        :param list1:
        :type list1: list of numbers
        :param list2:
        :type list2: list of numbers
        :return: average value
        """
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
        """
        Calculate the distribution of some data against given limits

        :param data:
        :type data: list of numbers
        :param limits: limits of categories
        :type limits: list of numbers
        :return: number of elements between [i]th and [i+1]th element
        """
        if data is None or limits is None:
            return None
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
        """
        Calculate the distribution of temperature data

        :param temps: temperature data
        :type temps: list of numbers
        :return: number of elements between [i]th and [i+1]th element of Climate.TEMP_DISTRIBUTION_LIMITS
        """
        data = Climate.calculate_distribution(temps, Climate.TEMP_DISTRIBUTION_LIMITS)
        return data

    @staticmethod
    def calculate_rh_distribution(rhs):
        """
        Calculate the distribution of relative humidity data

        :param rhs: relative humidity data
        :type rhs: list of numbers
        :return: number of elements between [i]th and [i+1]th element of Climate.RH_DISTRIBUTION_LIMITS
        """
        data = Climate.calculate_distribution(rhs, Climate.RH_DISTRIBUTION_LIMITS)
        return data

    @staticmethod
    def calculate_wind_distribution(winds):
        """
        Calculate the distribution of wind direction data

        :param rhs: wind direction data
        :type rhs: list of numbers
        :return: number of elements between [i]th and [i+1]th element of Climate.WIND_DIRECTION_LIMITS
        """
        data = Climate.calculate_distribution(winds, Climate.WIND_DIRECTION_LIMITS)
        return data

    @staticmethod
    def count_significants(significant, daily):
        """
        Counts number of significant weather events, increases initial dictionary

        :param significant: number of significant events {key: WEATHER_CODE.id, value: number}
        :type significant: dictionary
        :param daily: list of significant events existing ['WEATHER_CODE.id']
        :type daily: list
        :return: increased dictionary with number of significant events
        """
        if daily is None:
            return significant
        for code in Weather.WEATHER_CODE:
            number = significant.get(code[0], 0)
            if str(code[0]) in daily:
                number = number + 1
            significant[code[0]] = number
        return significant
