"""Log to file errors and exceptions."""

import pathlib
from datetime import datetime


class ExLogger():
    """Log errors and exeptions.

    :data PATH: A path to a log file
    :PATH type: str
    """

    PATH = pathlib.Path(".\\logs\\logs.txt")

    def __init__(self):
        """Create Logger object."""
        self._datetime = datetime.now()

    def log(self, obj: object) -> None:
        """Log errors and exeptions.

        :param obj: data to log
        :obj type: object
        """
        content = f"{self._datetime}: {str(obj)}"

        with open(ExLogger().PATH, 'a', encoding="utf-8") as file:
            file.write(content)
