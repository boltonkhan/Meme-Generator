"""Module responsible for scraping 'https://quotes.toscrape.com'.

The purpse is to build wilder base of quotes for the meme engine.
"""

import time
from typing import List

import requests
from bs4 import BeautifulSoup, Tag
from Models import QuoteModel
from Services.QuoteScrapper.QuoteScrapperInterface import \
    QuoteScrapperInterface


class QuoteToScrapScrapper(QuoteScrapperInterface):
    """Scrap quotes from the webpage.

    :data BASE_URL: quote to scrap home url
    :BASE_URL type: string
    :data DATA_STORAGE: file with scrapped data
    :DATA_STORAGE type: str
    """

    DATA_STORAGE = "./_data/Quotestoparse/quotes_toscrap.csv"
    BASE_URL = "https://quotes.toscrape.com"

    @classmethod
    def get_quotes(cls) -> List[QuoteModel]:
        """Get quotes from the side.

        :return: collection of found authors and quotes
        :rtype: `List[QuoteModel]`
        """
        quotes = []
        max_tries = 3
        try_no = 1
        time_to_wait = 10
        page = 1

        while True:  # as long as quote and author are found

            req_url = f"{cls.BASE_URL}/page/{page}"  # setup page no
            res = requests.get(req_url)  # make a request

            if res.ok:
                quotes_ = cls._parse(res.content)  # create QuoteModel list

                if quotes_:
                    quotes.extend(cls._parse(res.content))
                    page += 1
                else:
                    break

            elif res.status_code == 408:  # timeout
                if try_no <= max_tries:  # retry max 3 times
                    time_to_wait *= try_no
                    time.sleep(time_to_wait)
                    try_no += 1
                    continue
                else:
                    break
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
        body = quote.select_one(".text")
        body = body.text.strip('”“') \
            if body is not None \
            else None

        author = quote.select_one(".author")
        author = author.text.strip("-") \
            if author is not None \
            else None

        try:
            quote = QuoteModel(body, author)
        except AssertionError:  # quote is too long
            quote.body = None
            quote.author = None
        finally:
            return quote
