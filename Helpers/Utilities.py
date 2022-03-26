"""Additional function/helpers."""

import os
import pathlib
from numbers import Number
from random import choices, uniform
from string import ascii_letters, digits
from typing import List

import pandas as pd


def is_windows():
    """Check if system is Windows."""
    if os.name == 'nt':
        return True
    return False


def get_extension(path: str) -> str:
    """Get given file extension/type.

    :param path: A File path.
    :path type: str
    :return: extension/type of the file with ., e.g. '.ttf'
    :rtype: str
    """
    return pathlib.Path(path).suffix


def get_filename(path: str) -> str:
    """Extract file name.

    :param path: path
    :path type: str
    :return: file name or None
    :rtype: str
    """
    return pathlib.Path(path).name


def find_files_by_ext(
        base_dir: str, extension: str = None, dir_to_exclude: str = None
        ) -> List[str]:
    """Find all files. If extension is None return all files.

    If extension is defined function looks for files
    starting from location specified by `base_dir` catalogue.
    Searches recursively incluading subcatalogues.

    :param base_dir: Dir to start search in
    :base_dir type: str
    :param extension: Extension to find files with,
        can be with . or without, e.g. '.ttf' or 'ttf'
    :extension type: str, optional
    :param dir_to_exclude: Directory file from should be filtered.
        Only one value is supported
    :dir_to_exclude type: str, optional
    :return: List of relative paths to found files
    :rtype: List of str
    """
    def filter_files(paths: List[str], dir_: str) -> List[pathlib.Path]:
        split_by = None
        if is_windows():
            split_by = "\\"
        else:
            split_by = "/"

        paths = list(
            map(
                lambda path: str(pathlib.Path(path)).split(split_by), paths
            )
        )
        paths = list(
            filter(
                lambda path: True if path.count(dir_) == 0 else False, paths
            )
        )
        return list(map(lambda path: pathlib.Path('/'.join(path)), paths))

    paths = []

    dir_path = pathlib.Path(base_dir)

    if dir_path.is_dir():

        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:

                if extension is not None:  # extension defined
                    if file.endswith(extension):
                        paths.append(os.path.join(root, file))

                else:  # extension does not defined
                    paths.append(os.path.join(root, file))

    if dir_to_exclude:
        paths = filter_files(paths, dir_to_exclude)

    return paths


def save_bytes(content: bytes, path: str) -> str:
    """Save bytes to file.

    Create new file if not exists, overides existing file
    :param content: bytes to save
    :content type: bytes
    :param path: path to file
    :path type: str
    """
    path = pathlib.Path(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb+') as file:
        file.write(content)

    return path


def save_csv(json: str, path: str) -> None:
    """Create csv file from json data.

    :param json: json data to write
    :json type: str
    :param path: location a file to wite
    :path type: str
    """
    path = pathlib.Path(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.read_json(json)
    df.to_csv(path, index=False)


def round_up(value: Number) -> int:
    """Round up given value.

    :param value: value to round up
    :value type: Number
    :return: rouded up value as an int
    :rtype: int
    """
    return int(value + 0.5)


def build_random_str(lenght: int) -> str:
    """Build random string consists of ascii letters and numbers.

    :param lenght: count of characters
    :lenght type: int
    :return: string consists of andom chars
    :rtype: str
    """
    chars = list(ascii_letters)
    chars.extend(digits)
    name = choices(chars, k=lenght)
    return ''.join(name)


def draw_float(start: float, end: float) -> float:
    """Select draw float number from a given range.

    :param start: left limit of the range
    :start type: float
    :param end: right limit of the range
    :end type: float
    :return: random float number from a given range
    :rtype: float
    """
    return uniform(start, end)


def param_value_from_url(param: str, url: str) -> str:
    """Get param value from url.

    :param param: parameter name to value get for
    :param type: str
    :param url: url to parse
    :url type: str
    """
    url = url.lower()
    param = param.lower()
    result = [p.split('=')[1] for p in url.split('?')[1].split('&')
              if p.startswith(param)]
    if result:
        return result[0]
    return result
