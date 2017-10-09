class Climate(object):
	tempDistribLimits = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
	rhDistribLimits = [20, 40, 60, 80]
	windDirLimits = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]

	# input list of Tmins or list of Tmaxs
	def getNrFrostDays(minTemps):
		return len([x for x in minTemps if x != None and x < 0])
	def getNrColdDays(minTemps):
		return len([x for x in minTemps if x != None and x < -10])
	def getNrWarmNights(minTemps):
		return len([x for x in minTemps if x != None and x > 20])
	def getNrSummerDays(maxTemps):
		return len([x for x in maxTemps if x != None and x > 25])
	def getNrWarmDays(maxTemps):
		return len([x for x in maxTemps if x != None and x >= 30])
	def getNrHotDays(maxTemps):
		return len([x for x in maxTemps if x != None and x >= 35])

	@staticmethod
	def calculateDistribution(data, limits):
		res = []
		for i in range(len(limits)):
			if (i == 0):
	  			high = limits[i]
			elif (i == len(limits) - 1):
	  			low = limits[i]
			else:
	  			low = limits[i]
	  			high = limits[i+1]
			sublist = [x for x in data if x != None and (high == None or x <= high) and (low == None or x > low)]
			res.append(len(sublist))
		return res

	@staticmethod
	def calculateTempDistrib(temps):
		data = Climate.calculateDistribution(temps, Climate.tempDistribLimits)
		return data

	@staticmethod
	def calculateRhDistrib(rhs):
		data = Climate.calculateDistribution(rhs, Climate.rhDistribLimits)
		return data

	@staticmethod
	def calculateWindDistrib(rhs):
		data = Climate.calculateDistribution(rhs, Climate.windDirLimits)
		return data