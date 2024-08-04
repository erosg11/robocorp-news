from playwright.sync_api import JSHandle
from robocorp import log

from .NewsElement import NewsElement
from .NewsApp import NewsApp
from yarl import URL
from typing import Sequence


class ApNewsApp(NewsApp):
    BASE_URL = URL('https://apnews.com/search')

    def __init__(self, limit_date: str | int, **kwargs):
        super().__init__(limit_date, **kwargs)
        log.info('Starting new ApNews App')
        self.url = ApNewsApp.BASE_URL

    def close_popup(self):
        try:
            self.bc.click('.fancybox-item.fancybox-close', timeout=100)
        except Exception:
            log.info('No popup found, skiping...')
            pass

    def search(self, term: str):
        self.update_params(q=term, s=3, p=self.page)
        self.close_popup()

    def get_news(self) -> Sequence[NewsElement]:
        get_elements = True
        while get_elements:
            get_elements = False
            elements = self.bc.get_all('div.SearchResultsModule-results div.PagePromo')
            for element in elements:
                news = self.to_news_element(element)
                if news.date < self.limit_date:
                    log.info('Too old, skipping', news)
                    continue
                yield news
                get_elements = True
            if get_elements:
                self.next_page()

    def next_page(self):
        self.page += 1
        self.update_params(p=self.page)
        self.close_popup()

    def to_news_element(self, element: JSHandle) -> NewsElement:
        return NewsElement(
            title=self.bc.get_text_from_element(element, '.PagePromo-title'),
            description=self.bc.get_text_from_element(element, '.PagePromo-description'),
            date=int(self.bc.get_attribute_from_sub_element(
                element, 'bsp-timestamp', 'data-timestamp')) / 1000,
            picture_url=self.bc.get_attribute_from_sub_element(element, 'img', 'src'),
        )
