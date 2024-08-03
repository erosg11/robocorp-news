from datetime import date

from .NewsApp import NewsApp
from yarl import URL
from .ApNewsElement import ApNewsElement
from typing import Sequence


class ApNewsApp(NewsApp):
    BASE_URL = URL('https://apnews.com/search')

    def __init__(self, limit_date: str | int, **kwargs):
        super().__init__(limit_date, **kwargs)
        self.url = ApNewsApp.BASE_URL

    def close_popup(self):
        try:
            self.bc.click('.fancybox-item.fancybox-close', timeout=100)
        except Exception:
            pass

    def search(self, term: str):
        self.update_params(q=term, s=3, p=self.page)
        self.close_popup()

    def get_news(self) -> Sequence[ApNewsElement]:
        get_elements = True
        while get_elements:
            get_elements = False
            elements = self.bc.get_all('div.SearchResultsModule-results div.PagePromo')
            for element in elements:
                news = ApNewsElement.from_element(element)
                if news.date < self.limit_date:
                    continue
                yield news
                get_elements = True
            if get_elements:
                self.next_page()

    def next_page(self):
        self.page += 1
        self.update_params(p=self.page)
        self.close_popup()
