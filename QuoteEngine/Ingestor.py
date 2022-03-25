"""Implements IngestorInterface and encapsulates helper classes."""

from typing import List

from Helpers import Utilities as util
from Models.QuoteModel import QuoteModel

from .CsvIngestor import CsvIngestor
from .CustomErrors import UnsupportedFileError
from .DocxIngestor import DocxIngestor
from .IngestorInterface import IngestorInterface
from .PdfIngestor import PdfIngestor
from .TextIngestor import TextIngestor


class Ingestor(IngestorInterface):
    """Encapsulate quote engine logic.

    :data INGESTORS: collection of all IngestorInterface classes
    :data type: List[IngestorInterface]
    """

    INGESTORS = [
        CsvIngestor,
        DocxIngestor,
        PdfIngestor,
        TextIngestor
    ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return specific parser for the given file type.

        :param path: path to the file
        :path type: str
        :return: collection of `QuoteModel`
        :rtype: List[QuoteModel]
        :raises UnsupportedFileError: engine does not support
            file with the extentinon
        """
        format = util.get_extension(path)  # extract extension from path

        for ingestor in cls.INGESTORS:  # find proper ingestor for the file

            if format in ingestor.__dict__.get("SUPPORTED_FORMATS", False):
                return ingestor.parse(path)

        raise UnsupportedFileError(f"File format: {format} is not supported!")

    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Get file formats support by the Ingestor factory.

        :return: list of supported file formats
        rtype: str
        """
        supported_files = []

        for ingestor in cls.INGESTORS:
            supported_files.extend(
                ingestor.__dict__.get("SUPPORTED_FORMATS", None)
            )

        return [file for file in supported_files if file is not None]
