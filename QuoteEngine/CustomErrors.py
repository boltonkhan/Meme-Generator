"""Cutrom errors classes for QuoteEngine."""


class UnsupportedFileError(ValueError):
    """Represent error of trying to ingest unsupported file type.

    :param msg: error message
    :param type: str
    """

    def __init__(self, msg: str) -> None:
        """Create an object od the class."""
        super().__init__()
        self.msg = msg

    def __str__(self):
        """Represent {str} of the object."""
        return self.msg


class WrongFileStructureError(ValueError):
    """Raise when file content in a wrong structure/format.

    :param msg: error message
    :param type: str
    """

    def __init__(self, msg: str) -> None:
        """Create an object od the class."""
        super().__init__()
        self.msg = msg

    def __str__(self):
        """Represent {str} of the object."""
        return f"{self.__dict__}"
