class Number:
    """
    Helper class for handling numbers as strings
    """

    @staticmethod
    def is_number(string):
        """
        check a string if it contains a number
        :param string: input e.g. '1', 'n2kj34', '9.99'
        :return: True or False
        """
        if string is None:
            return False
        try:
            float(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def to_float(string):
        """
        parse a string to float
        :param string:
        :return: number
        """
        if string is None:
            return None
        try:
            return float(string)
        except ValueError:
            return None

    @staticmethod
    def to_int(string):
        """
        parse a string to integer
        :param string:
        :return:
        """
        if string is None:
            return None
        try:
            return int(string)
        except ValueError:
            return None
