"""Custom error - provided text is too long.

Raises when provided text to draw on an image is too long
in comparison to image size and font style and size
"""


class TextTooLongError(ValueError):
    """Raise error when given text is too long."""

    def __init__(self, msg: str) -> None:
        """Create an instance."""
        super().__init__()
        self.msg = msg

    def __str__(self):
        """Return string format of the exception."""
        return f"{self.msg}"
