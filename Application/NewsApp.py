from abc import ABC, abstractmethod
from typing import Sequence

from robocorp import log
from yarl import URL
from dateutil.relativedelta import relativedelta

from .NewsElement import NewsElement
from Controllers import BrowserController
from playwright.sync_api import JSHandle
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=0))


class NewsApp(ABC):
    matches: list[JSHandle] = []
    page = 1
    params: dict[str, str | int] | None = None

    def __init__(self, limit_date: str | int, **kwargs):
        self.limit_date = datetime.fromisoformat(limit_date) \
            if isinstance(limit_date, str) else datetime.now(tz=TZ) - relativedelta(months=limit_date)
        self.params = {}
        self.url: URL | None = None
        self.bc = BrowserController(**kwargs)

    def update_params(self, **kwargs):
        self.params |= kwargs
        self.url = self.url.update_query(self.params)
        log.info('Going to', self.url)
        self.bc.open(str(self.url))

    @abstractmethod
    def search(self, term: str):
        raise NotImplementedError('Search method must be implemented')

    @abstractmethod
    def get_news(self) -> Sequence[NewsElement]:
        raise NotImplementedError('get_news method must be implemented')

    @abstractmethod
    def next_page(self):
        raise NotImplementedError('next_page method must be implemented')

    @abstractmethod
    def to_news_element(self, element: JSHandle) -> NewsElement:
        raise NotImplementedError('to_news_element method must be implemented')
