"""A part of a QuoteEngine module for txt files.

The QuoteEngine module is responsible for
ingesting many types of files that contain quotes.
"""
from typing import List

from Helpers.ExLogger import ExLogger
from Models.QuoteModel import QuoteModel

from QuoteEngine.CustomErrors import WrongFileStructureError

from .IngestorInterface import IngestorInterface


class TextIngestor(IngestorInterface):
    """An infractructure to process txt files.

    :data SUPPORTED_FORMATS: collection of supported files
    :data type: List[str]
    """

    SUPPORTED_FORMATS = ['.txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse txt file.

        :param path: path to the file
        :path type: str
        :return: collection of quotes and authors
        :rtype: List[QuoteModel]
        """
        quotes = []

        # `utf-8-sig` to avoid unwanted chars
        with open(path, "r", encoding="utf-8-sig") as file:
            data = TextIngestor().clean_data(file.read())  # prepare data
            quote = None
            for data_row in data:
                try:
                    quote = cls.map_to_quote(data_row)

                except WrongFileStructureError as e:
                    quote = None
                    e.__dict__["file_name"] = path
                    ExLogger().log(e)

                finally:
                    if quote:
                        quotes.append(quote)

        return quotes

    @classmethod
    def clean_data(cls, data: str) -> List[str]:
        """Clean data uploaded from txt file.

        Remove all unwanted chars and
        prepare the data to parse them to QuoteModel obj.
        :param data: data to clean
        :data type: str
        :return: collection of strings
        :rtype: List[str]
        """
        # split test into lines and each line into text splitted with dash
        data = [elem.split("-") for elem in data.splitlines()]

        # remove whitespaces and additional quote chars
        return [[pos.strip().strip("\"") for pos in elem] for elem in data]

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if given file is supported.

        :param path: path to file
        :path type: str
        :return: True if file is supported, otherwise False
        :rtype: bool
        """
        return super().can_ingest(path)

    @classmethod
    def map_to_quote(cls, data_row: List[str]) -> QuoteModel:
        """Map row of txt data to QuoteModel object.

        :param data_row: line from the file
        :data type: str
        :return: quote and autor
        :rtype: `QuoteModel` object.
        :raises WrongFileStructureError: can't tranform data
            to `QuoteModel` object.
        """
        if len(data_row) != 2:  # 2 elements expected

            raise WrongFileStructureError(
                f"Wrong file structure. Expected: <body> - <quote>."
                f"Provided: {data_row}"
            )

        body = data_row[0]  # quote
        author = data_row[1]  # author

        return QuoteModel(body, author)
