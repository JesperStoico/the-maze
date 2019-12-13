import os


def is_win() -> bool:
    """ Return True if OS is Windows """
    return True if os.name == "nt" else False


def check_os_path():
    """Finds correct maze path"""
    if is_win():
        return "\\"
    else:
        return "/"
