from django.db import models

from urllib.parse import urlencode
import hashlib
import urllib
def gravatar_url(email, size=100):
	email = email.lower().encode("utf-8")
	default = "identicon"
	return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))

class Weather(models.Model):
	WEATHER_CODE = (
	(1, 'füst'), (2, 'homály'), (3, 'párásság'), (4, 'köd'), (19, 'nyílt köd'), (13, 'homokvihar'), (14, 'porforgatag'), 
	(5, '22-es halo'), (6, 'melléknap'), (7, 'érintő ív'), (8, 'ritkább halo'),
	(9, 'villámlás'), (10, 'dörgés'), (11, 'szivárvány'), (12, 'csapadéksáv'),
	(15, 'szitálás'), (16, 'szemcsés hó'), (17, 'ónos szitálás'), (34, 'ónos eső'),
	(18, 'eső'), (20, 'havazás'), (22, 'havas eső'),
	(24, 'zápor'), (25, 'hózápor'), (26, 'havas eső zápor'), (27, 'jégeső'),
	(29, 'tuba'), (30, 'tornádó'), (31, 'zivatar'), (32, 'hódara-zápor'), (33, 'fagyott eső'),
	(34, 'harmat'), (35, 'dér'), (36, 'zúzmara'), (37, 'hófúvás')
	)

	BEAUFORT_SCALE = (
	(-1, 'nem észlelt'),
	(0, '0: szélcsend'), (1, '1: füst lengedezik'), (2, '2: arcon érezhető'), (3, '3: vékony gallyak mozognak'),
	(4, '4: kisebb ágak mozognak'), (5, '5: nagyobb ágak mozognak, suhog'), (6, '6: drótkötelek zúgnak, vastag ágak mozognak'),
	(7, '7: gallyak letörnek'), (8, '8: ágak letörnek'), (9, '9: gyengébb fák kidőlnek, épületekben kisebb károk'),
	(10, '10: fák gyökerestül kidőlnek'), (11, '11: súlyos károk'), (12, '12: súlyos pusztítás')
	)
	
	def getWeatherCodeText(ndx):
		if type(ndx) == str and ndx != '':
			ndx = int(ndx)
		find = [x[1] for x in Weather.WEATHER_CODE if x[0] == ndx]
		if len(find) > 0:
			return find[0]