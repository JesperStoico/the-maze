from os import name


def is_win() -> bool:
    """ Return True if OS is Windows """
    return True if name == "nt" else False
