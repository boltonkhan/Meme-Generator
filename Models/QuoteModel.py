"""Data model for quotes."""


class QuoteModel():
    """Represent data model for quotes."""

    def __init__(self, body: str, author: str) -> None:
        """Construct an object of QuoteModel class.

        Lenght of <body author> can't be higher than 300 chars
        :param body: A quote
        :type body: str
        :param author: An author of the quote
        :author type: str
        :return: `QuoteModel` instance
        """
        self.body = body
        self.author = author

        assert len(self) <= 300, \
            "Both the body and the author combined can't exceed 300 chars."

    def __len__(self) -> int:
        """Return char count in QuoteModel object.

        The lenght is for the format `{body} {autor}`,
        with one space and without qoute marks and additinal chars.
        return: char count
        rtype: int
        """
        return len(f"{self.body} {self.author}")

    def __repr__(self) -> str:
        """Return string representation of a QuoteModel."""
        return f"{self.body}-{self.author}"

    def __str__(self) -> str:
        """Return string representation of a QuoteModel."""
        return f"{self.body}-{self.author}"
