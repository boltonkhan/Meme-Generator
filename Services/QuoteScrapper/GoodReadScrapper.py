"""Module responsible for scraping 'https://www.goodreads.com/'.

The purpse is to build wilder base of quotes for the meme engine.
"""

import re
import time
from random import choice
from typing import List

import requests
from bs4 import BeautifulSoup, Tag
from Models import QuoteModel
from Services.QuoteScrapper.QuoteScrapperInterface import \
    QuoteScrapperInterface


class GoodReadScrapper(QuoteScrapperInterface):
    """Scrap quotes from the webpage.

    :data BASE_URL: quote to scrap home url
    :BASE_URL type: string
    """

    BASE_URL = "https://www.goodreads.com/quotes"

    @classmethod
    def get_quotes(cls) -> List[QuoteModel]:
        """Get quotes from the side.

        One random page (from 1 to 100 range) is scrapped
        :return: collection of found authors and quotes
        :rtype: `List[QuoteModel]`
        """
        quotes = []
        max_tries = 3
        try_no = 1
        time_to_wait = 10
        page_no = choice(range(1, 100))  # draw a page no

        payload = {'page': page_no}
        res = requests.get(cls.BASE_URL, payload)  # make a request

        if res.ok:
            quotes = cls._parse(res.content)  # create QuoteModel list

        elif res.status_code == 408:  # timeout
            if try_no <= max_tries:  # retry max 3 times
                time_to_wait *= try_no
                time.sleep(time_to_wait)
                try_no += 1

        else:  # sth goes wrong
            raise requests.HTTPError(res.status_code)

        return quotes

    @classmethod
    def filter_empty(cls, quotes: List[QuoteModel]) -> List[QuoteModel]:
        """Filter None elements from `List[QuoteModel]`.

        If either body is None or author is None, remove it from the list.
        :param quotes: a collection of `List[QuoteModel]` to filter
        :quotes type: `List[QuoteModel]`
        :return: a collection of found author and quotes
        :rtype: `List[QuoteModel]`
        """
        return super().filter_empty(quotes)

    @classmethod
    def _parse(cls, content: bytes) -> List[QuoteModel]:
        """Parse the content.

        :param content: full response
        :content type: bytes
        :return: a collection of found author and quotes
        :rtype: `List[QuoteModel]`
        """
        soup = BeautifulSoup(content, 'html.parser')
        quotes = soup.select(".quote")

        return cls.filter_empty(
            list(map(cls._extract_quotemodel, quotes))
            )

    @classmethod
    def _extract_quotemodel(cls, quote: Tag) -> List[QuoteModel]:
        """Extract quote and model.

        :param quote: full element with quote and author html element
        :quote type: `bs4.Tag`
        :return: a collection of found author and quotes
        :rtype: `List[QuoteModel]`
        """
        group = quote.select_one(".quoteText")

        body_pattern = re.compile(r"“.*”")
        body = re.search(body_pattern, group.text)\
            .group(0).strip('“”“”')
        author = group.select_one(".authorOrTitle")\
            .text.strip(' \n,')

        try:
            quote = QuoteModel(body, author)
        except AssertionError:  # quote is too long
            quote = QuoteModel(None, None)
        finally:
            return quote
