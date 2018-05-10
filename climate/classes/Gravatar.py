from urllib.parse import urlencode
import hashlib


class Gravatar:
    """
    | Helper class for generating gravatar URL
    """
    ICON_SET = "identicon"
    URL_TEMPLATE = "https://www.gravatar.com/avatar/%s?%s"

    @staticmethod
    def get_gravatar_url(email, size=100):
        """
        Generate gravatar URL

        :param email: e-mail address of a user
        :type email: string
        :param size: size of the requested avatar image
        :type size: number
        :return: URL of avatar image
        """
        email = email.lower().encode("utf-8")
        param1 = hashlib.md5(email.lower()).hexdigest()
        param2 = urlencode({'d': Gravatar.ICON_SET, 's': str(size)})
        return Gravatar.URL_TEMPLATE % (param1, param2)
