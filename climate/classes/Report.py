class Report():
    def getNrOfSnowDays(self):
        s = 0
        for j in self.manualDayObjs:
            if j.isSnow:
                s = s + 1
        return s
