"""A part of a QuoteEngine module.

The QuoteEngine module is responsible for
ingesting many types of files that contain quotes.
"""
from typing import List

from docx import Document
from Helpers import ExLogger
from Models.QuoteModel import QuoteModel

from .CustomErrors import WrongFileStructureError
from .IngestorInterface import IngestorInterface


class DocxIngestor(IngestorInterface):
    """An infractructure to process docx files."""

    SUPPORTED_FORMATS = [".docx"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse docx file.

        :param path: `.docx`file path
        :path type: str
        :return: a `QuoteModel` collection
        :rtype: List[QuoteModel]
        """
        quotes = []  # quotes to return

        document = Document(path)  # object to work with

        for par in document.paragraphs:  # iterate each paragaph
            data = DocxIngestor.clean_data(par.text)  # prepare uploaded data
            if data:
                try:
                    quotes.append(
                        cls.map_to_quote(data)
                    )
                except ValueError as e:
                    ExLogger().log(e)  # log error

        return quotes

    @classmethod
    def clean_data(cls, data: str) -> List[str]:
        """Clean and prepare data from the file.

        :param data: string loaded from the file
        :data type: str
        :return: collection of strings
        :rtype: List[str]
        """
        # split text to author and quote
        data = data.split("-")  # expected <autor> - <quote>
        return [elem.strip().strip("\"") for elem in data if elem]

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if given file is supported.

        :param path: path to the file
        :path type: str
        :return: True if extension is supported,
            otherwise False
        :rtype: bool
        """
        return super().can_ingest(path)

    @classmethod
    def map_to_quote(cls, data_row: List[str]) -> QuoteModel:
        """Map row of the data to QuoteModel object.

        :param data_row: a row of file data
        :data_row type: List[str]
        :return: a `QuoteModel` object
        :rtype: QuoteModel
        :raises WrongFileStructureError: can't transform data row to object
        """
        if len(data_row) != 2:  # 2 elements expected

            raise WrongFileStructureError(
                f"Wrong file structure. Expected: <body> - <quote>. "
                f"Provided: {data_row}"
            )

        body = data_row[0]  # the quote
        author = data_row[1]  # author of the quote

        return QuoteModel(body, author)
