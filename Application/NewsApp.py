"""Base application to collect news data"""

from abc import ABC, abstractmethod
from typing import Sequence

from loguru import logger
from yarl import URL
from dateutil.relativedelta import relativedelta

from entitys import NewsElement
from Controllers import BrowserController
from playwright.sync_api import JSHandle
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=0))


class NewsApp(ABC):
    """NewsApp base class to collect news data"""
    page = 1
    params: dict[str, str | int] | None = None
    search_phrase: str | None = None

    def __init__(self, limit_date: str | int, **kwargs):
        """
        Initialize the NewsApp class
        :param limit_date: The date limit to collect news data for
        :param kwargs: Arguments passed to the browser class
        """
        self.limit_date = datetime.fromisoformat(limit_date) \
            if isinstance(limit_date, str) else datetime.now(tz=TZ) - relativedelta(months=limit_date)
        self.params = {}
        self.url: URL | None = None
        self.bc = BrowserController(**kwargs)

    def update_params(self, **kwargs):
        """Update the params dict with new params and open the url based in the new params"""
        self.params |= kwargs
        self.url = self.url.update_query(self.params)
        logger.info('Going to {!r}', self.url)
        self.bc.open(str(self.url))

    @abstractmethod
    def search(self, term: str):
        """
        Search news data for the term
        :param term: The term to search for
        """
        raise NotImplementedError('Search method must be implemented')

    @abstractmethod
    def get_news(self) -> Sequence[NewsElement]:
        """
        Get news data in current page
        :return: The news elements found that match the search term and limit date
        """
        raise NotImplementedError('get_news method must be implemented')

    @abstractmethod
    def next_page(self):
        """Go to the next page"""
        raise NotImplementedError('next_page method must be implemented')

    @abstractmethod
    def to_news_element(self, element: JSHandle) -> NewsElement:
        """Convert element to NewsElement"""
        raise NotImplementedError('to_news_element method must be implemented')
