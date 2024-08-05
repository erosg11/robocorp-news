from warnings import deprecated

from selenium.webdriver.remote.webelement import WebElement

from Controllers import BrowserController
from .NewsElement import NewsElement


@deprecated('Deprecated class, you should use ApNewsApp.to_news_element')
class ApNewsElement(NewsElement):

    @classmethod
    def from_element(cls, element: WebElement | None = None):
        return cls(
            title=BrowserController.get_text_from_element(element, '.PagePromo-title'),
            description=BrowserController.get_text_from_element(element, '.PagePromo-description'),
            date=int(BrowserController.get_attribute_from_sub_element(
                element, 'bsp-timestamp', 'data-timestamp')) / 1000,
            picture_url=BrowserController.get_attribute_from_sub_element(element, 'img', 'src'),
        )
