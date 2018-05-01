class Report:
    def get_nr_of_snow_days(self):
        s = 0
        for j in self.manualDayObjs:
            if j.isSnow:
                s = s + 1
        return s


