
def is_number(s):
    """ if s is a number, return True
        TESTED
    """
    if (is_float(s) or is_int(s)):
        return True
    return False

def is_float(s):
    """ if s is a float, return True
        TESTED
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_int(s):
    """ if s is an int, return True
        TESTED
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
