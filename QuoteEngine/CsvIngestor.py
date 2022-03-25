"""A part of a QuoteeEngine module.

The QuoteEngine module is responsible for
ingesting many types of files that contain quotes.
"""
from typing import List

import pandas as pd
from Models.QuoteModel import QuoteModel

from QuoteEngine.CustomErrors import WrongFileStructureError

from .IngestorInterface import IngestorInterface


class CsvIngestor(IngestorInterface):
    """An infractructure to process csv files."""

    SUPPORTED_FORMATS = [".csv"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse csv file.

        :param path: path to csv file
        :path type: str
        :return: Collection of `QuoteModel` objects
        :rtype: List[QuoteModel]
        """
        data = []
        try:
            data = pd.read_csv(
                path, usecols=["body", "author"], encoding="utf-8"
            )

        except ValueError:  # map value error to custom error

            raise WrongFileStructureError(
                f"File content is not ingestible. "
                f"Expect comma separated file with columns: "
                f"'body' and 'author'."
            )

        else:  # file in proper structure, map and check values
            quotes = list(map(cls.data_to_quotemodel, data.values.tolist()))
            quotes = list(  # filer None results
                filter(
                    lambda q: True if q.body is not None
                    and q.author is not None else False,
                    quotes
                )
            )

            return quotes  # return only good quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if given file is supported.

        :param path: path to the file
        :path type: str
        :return: True if the class supports file extension,
            otherwise False
        :rtype: bool
        """
        return super().can_ingest(path)

    @classmethod
    def data_to_quotemodel(cls, data: List[str]) -> List[QuoteModel]:
        """Map file data into QuoteModel object."""
        try:

            if any(str(c) == 'nan' for c in data):  # empty element exists
                quotemodel = QuoteModel(None, None)

            # there is no letters in at least one cell
            elif not all([any(str(char).isalpha() for char in str(elem))
                         for elem in data]):
                quotemodel = QuoteModel(None, None)

            else:
                quotemodel = QuoteModel(data[0], data[1])

        except AssertionError:
            quotemodel = QuoteModel(None, None)

        except ValueError as e:
            raise ValueError(e)

        finally:
            return quotemodel
