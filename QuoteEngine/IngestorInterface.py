"""A part of a QuoteeEngine module.

The QuoteEngine module is responsible for
ingesting many types of files that contain quotes.
"""
from abc import ABC, abstractmethod
from typing import List

from Helpers import Utilities as util
from Models.QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Abstract base class for all class responsible for parsing files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if given file is supported.

        :param path: path to file
        :path type: str
        :return: True if file supported, otherwise False
        :rtype: bool
        """
        file_format = util.get_extension(path)  # get file extension

        if file_format not in cls.__dict__.get("SUPPORTED_FORMATS", False):
            return False

        return True

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Abstract method to parse given file.

        :param path: path to file
        :path type: str
        :return: collection of `QuoteModel` objects
        :rtype: List[QuoteModel]
        """
        pass
