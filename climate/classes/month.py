from django.utils import timezone
import calendar

class Month:
	def __init__(self, now=timezone.now(), year=0, month=0):
		if year == 0 or month == 0:
			self.year = now.year
			self.month = now.month
		else:
			self.year = int(year)
			self.month = int(month)
	def getDateReadable(self):
		return str(self.year) + "." + str(self.month) + "."
	def isInMonth(self, dt):
		return self.year == dt.year and self.month == dt.month
	def daysOfMonth(self):
		lastDay = calendar.monthrange(self.year, self.month)[1]
		a = []
		[a.append(i) for i in range(1, lastDay + 1)]
		return a
	def daysOfMonthTillToday():
		lastDay = timezone.now().day
		a = []
		[a.append(i) for i in range(1, lastDay + 1)]
		return a
	def getMonth(self):
		return str(self.month).zfill(2)