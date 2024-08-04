from warnings import deprecated

from Controllers import BrowserController
from .NewsElement import NewsElement

from playwright.sync_api import JSHandle


@deprecated('Deprecated class, you should use ApNewsApp.to_news_element')
class ApNewsElement(NewsElement):

    @classmethod
    def from_element(cls, element: JSHandle | None = None):
        return cls(
            title=BrowserController.get_text_from_element(element, '.PagePromo-title'),
            description=BrowserController.get_text_from_element(element, '.PagePromo-description'),
            date=int(BrowserController.get_attribute_from_sub_element(
                element, 'bsp-timestamp', 'data-timestamp')) / 1000,
            picture_url=BrowserController.get_attribute_from_sub_element(element, 'img', 'src'),
        )
