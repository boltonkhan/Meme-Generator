"""Cutrom errors/exception class raises when given image is not supported."""


class UnsuportedImageError(ValueError):
    """Raise when image is not supported.

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
