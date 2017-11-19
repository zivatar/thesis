from django.utils import timezone
import calendar

class Month:
	def __init__(self, now=timezone.now(), year=0, month=0):
		if year == 0 or month == 0:
			self.year = now.year
			self.month = now.month
			self._currentMonth = True
		else:
			self.year = int(year)
			self.month = int(month)
			self._currentMonth = False
	def getDateReadable(self):
		return str(self.year) + "." + str(self.month) + "."
	def isInMonth(self, dt):
		return self.year == dt.year and self.month == dt.month
	def lastDay(self): # TODO test
		return calendar.monthrange(self.year, self.month)[1]
	def daysOfMonth(self):
		lastDay = calendar.monthrange(self.year, self.month)[1]
		a = []
		[a.append(i) for i in range(1, lastDay + 1)]
		return a
	def daysOfMonthTillToday(self):
		if self._currentMonth:
			lastDay = timezone.now().day
		else:
			lastDay = calendar.monthrange(self.year, self.month)[1]
		a = []
		[a.append(i) for i in range(1, lastDay + 1)]
		return a
	def getMonth(self):
		return str(self.month).zfill(2)