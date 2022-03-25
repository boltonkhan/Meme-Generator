"""Cutrom errors/exceptions classes for Services."""


class InvalidUrlError(ValueError):
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
