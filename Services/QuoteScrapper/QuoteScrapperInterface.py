"""Provide interface for quotes scrappers."""

from abc import ABC, abstractmethod
from typing import List

from Models import QuoteModel


class QuoteScrapperInterface(ABC):
    """Provide interface for quotes scrappers.

    :data BASE_URL: base webpage url
    :BASE_URL type: str
    """

    @classmethod
    @abstractmethod
    def get_quotes(cls) -> List[QuoteModel]:
        """Get quotes from the webpage.

        :return: a collection of quotes and authors
        :rtype: `List[QuoteModel]`
        """
        pass

    @classmethod
    def filter_empty(cls, quotes: List[QuoteModel]) -> List[QuoteModel]:
        """Filter None elements from `List[QuoteModel]`.

        If either body is None or author is None, remove it from the list.
        :param quotes: a collection of `List[QuoteModel]` to filter
        :quotes type: `List[QuoteModel]`
        :return: a collection of found author and quotes
        :rtype: `List[QuoteModel]`
        """
        return list(
            filter(
                lambda qm: False if qm.body is None or qm.author is None
                else True, quotes
            )
        )
