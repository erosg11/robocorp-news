"""Application to read the apnews"""

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from entitys import NewsElement
from .NewsApp import NewsApp
from yarl import URL
from typing import Sequence


class ApNewsApp(NewsApp):
    """Application class to read the apnews"""
    BASE_URL = URL('https://apnews.com/search')

    def __init__(self, limit_date: str | int, browser_timeout: float=30, **kwargs):
        """
        Initialize the ApNewsApp.
        :param limit_date: Date limit to look news for
        :param kwargs: Arguments to pass to Browser
        """
        super().__init__(limit_date, browser_timeout, **kwargs)
        logger.info('Starting new ApNews App')
        self.url = ApNewsApp.BASE_URL

    def close_popup(self):
        """Close the annoying popup"""
        try:
            self.bc.click('css:.fancybox-item.fancybox-close')
        except Exception:
            logger.info('No popup found, skiping...')
            pass

    def get_categories(self) -> dict[str, str]:
        filter_ = self.bc.get_all('xpath://ul[@class="SearchFilter-items"]')

        if not filter_:
            logger.warning('Not found filter')
            return {}

        filter_ = filter_[0]

        categories = self.bc.run_js(
            'return Array.from(document.getElementsByClassName("CheckboxInput")).map((x) => (x.innerText));')

        checkboxes = filter_.find_elements(By.CSS_SELECTOR, 'div.CheckboxInput')

        uuids = [x.find_element(By.CSS_SELECTOR, 'input').get_attribute('value') for x in checkboxes]
        filters = {c: u for c, u in zip(categories, uuids)}
        return filters

    def search(self, term: str, categories: list[str] | None = None):
        """Search apnews for a term"""
        self.update_params(q=term, s=3, p=self.page)
        self.close_popup()
        if categories:
            site_categories = self.get_categories()
            uuids_to_search = []
            append_uuid_to_search = uuids_to_search.append
            for c in categories:
                site_category = site_categories.get(c.upper())
                if site_category is None:
                    logger.warning('Category {!r} not found', c)
                    continue
                append_uuid_to_search(site_category)
            if not uuids_to_search:
                raise ValueError('No categories found')
            self.update_params(f2=uuids_to_search)
            self.close_popup()
        self.search_phrase = term

    def get_news(self) -> Sequence[NewsElement]:
        """Get the news elements from the current page in apnews"""
        get_elements = True
        while get_elements:
            get_elements = False
            elements = self.bc.get_all('css:div.SearchResultsModule-results div.PagePromo')
            for element in elements:
                news = self.to_news_element(element)
                if news.date < self.limit_date:
                    logger.info('Too old, skipping {!r}', news)
                    continue
                yield news
                get_elements = True
            if get_elements:
                self.next_page()

    def next_page(self):
        """Open the next page in apnews"""
        self.page += 1
        self.update_params(p=self.page)
        self.close_popup()

    def to_news_element(self, element: WebElement) -> NewsElement:
        """Convert the apnews element into a NewsElement"""
        return NewsElement(
            title=self.bc.get_text_from_element(element, '.PagePromo-title'),
            description=self.bc.get_text_from_element(element, '.PagePromo-description'),
            date=int(self.bc.get_attribute_from_sub_element(
                element, 'bsp-timestamp', 'data-timestamp')) / 1000,
            picture_url=self.bc.get_attribute_from_sub_element(element, 'img', 'src'),
            search_phrase=self.search_phrase,
        )
