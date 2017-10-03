from urllib.parse import urlencode
import hashlib
import urllib

def gravatar_url(email, size=100):
	email = email.lower().encode("utf-8")
	default = "identicon"
	return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))