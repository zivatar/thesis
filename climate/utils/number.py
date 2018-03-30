"""
check a string if it contains a number
string: string
"""


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


"""
Parse a string to float
string: string
"""


def to_float(string):
    if string is None:
        return None
    try:
        return float(string)
    except ValueError:
        return None


"""
Parse an int to float
string: string
"""


def to_int(string):
    if string is None:
        return None
    try:
        return int(string)
    except ValueError:
        return None
