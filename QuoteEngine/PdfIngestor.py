"""A part of a QuoteEngine module responsible for pdf files.

The QuoteEngine module is responsible for
ingesting many types of files that contain quotes.
"""
import subprocess
from asyncio.subprocess import PIPE
from typing import List

from Models.QuoteModel import QuoteModel

from .CustomErrors import WrongFileStructureError
from .IngestorInterface import IngestorInterface


class PdfIngestor(IngestorInterface):
    """An infractructure to process pdf files.

    :data SUPPORTED_FORMATS: supported file extensions
    """

    SUPPORTED_FORMATS = [".pdf"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse pdf file.

        :param path: path to pdf file
        :param type: srt
        :return: a collection of `QuoteModel` objects
        :rtype: List[`QuoteModel`]
        """
        quotes = []

        with subprocess.Popen(
            ["pdftotext", path, "-"],  # the command
            stdout=PIPE,
            stderr=PIPE
        ) as proc:

            try:
                out, err = proc.communicate(timeout=15)

            except TimeoutError:
                proc.kill()  # kill the process
                out, err = proc.communicate()

            else:
                data = PdfIngestor.clean_data(out.decode("utf-8"))  # prepare

                for data_row in data:
                    quotes.append(
                        cls.map_to_quote(data_row)  # map to QuoteModel
                    )

        return quotes

    @classmethod
    def clean_data(cls, data: str) -> List[str]:
        """Clean data uploaded from pdf file.

        Remove all unwanted chars and
        prepare the data to parse them to QuoteModel obj.
        :param data: uploaded data file
        :data type: str
        :return: collection of str contains quotes and autors
        :rtype: List[str]
        """
        data = data.splitlines()  # split line-by-line
        data = [elem for elem in data if elem]  # remove empty
        data = [elem.split('-') for elem in data]  # dash as separator
        data = [[pos.strip() for pos in elem] for elem in data]  # strip
        # remove quotes
        return [[pos.strip("\"") for pos in elem] for elem in data]

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if given file is supported.

        :param path: path to file
        :path type: str
        :return: True if file supported, otherwise False
        :rtype: bool
        """
        return super().can_ingest(path)

    @classmethod
    def map_to_quote(cls, data_row: List[str]) -> QuoteModel:
        """Map row of the data to QuoteModel object.

        :param data_row: a row data file
        :data_row type: List[str]
        :return: `QuoteModel` object
        :rtype: QuoteModel
        :raises WrongFileStructureError: can't transform data row
            to `QuoteModel` object.
        """
        if len(data_row) != 2:  # 2 elements expected

            raise WrongFileStructureError(
                expected="<string value> - <string value>",
                value=data_row,
                details=str(cls)
            )

        body = data_row[0]  # quote
        author = data_row[1]  # autor

        return QuoteModel(body, author)
