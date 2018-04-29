from urllib.parse import urlencode
import hashlib


class Gravatar:
    ICON_SET = "identicon"
    URL_TEMPLATE = "https://www.gravatar.com/avatar/%s?%s"

    @staticmethod
    def get_gravatar_url(email, size=100):
        email = email.lower().encode("utf-8")
        param1 = hashlib.md5(email.lower()).hexdigest()
        param2 = urlencode({'d': Gravatar.ICON_SET, 's': str(size)})
        return Gravatar.URL_TEMPLATE % (param1, param2)
