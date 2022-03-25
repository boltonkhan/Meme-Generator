"""Cutrom error raises when config file for a service is not found."""


class InvalidConfigFileError(FileNotFoundError):
    """Raise when url has wrong format.

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
