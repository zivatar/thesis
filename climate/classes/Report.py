class Report:
    """
    Report class to create report to display from raw and aggregated data
    """

    def get_nr_of_snow_days(self):
        """
        | Get the number of days with snow coverage

        :return: number of days
        """
        s = 0
        for j in self.manualDayObjs:
            if j.isSnow:
                s = s + 1
        return s


