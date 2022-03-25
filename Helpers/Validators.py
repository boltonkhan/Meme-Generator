"""Validators - validation functions."""
import re


def is_url(url: str) -> bool:
    """Check if url is valid.

    :param url: url address
    :url type: str
    :return: True if url is valid, otherwise False
    :rtype: bool
    """
    # based on https://stackoverflow.com/questions/7160737
    regex = re.compile(
        r"(https?|ftp)://"  # protocol
        r"(\w+(\-\w+)*\.)?"  # host (optional)
        r"((\w+(\-\w+)*)\.(\w+))"  # domain
        r"(\.\w+)*"  # top-level domain (optional, can have > 1)
        r"([\w\-\._\~/]*)*(?<!\.)"  # path, params, anchors, etc. (optional)
    )

    return bool(re.match(regex, url))


def is_filename(name: str) -> bool:
    """Check if the name is valid filename.

    Support filenames with extensions only!
    :param name: string to check
    :name type: str
    :return: True is name is a filename, otherwise False
    :rype: bool
    """
    regex = re.compile(r'^[\w,\s-]+\.[A-Za-z]{2,}$')

    return bool(re.match(regex, name))
