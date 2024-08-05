"""Controller layer to Browser module."""
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from yarl import URL

from DataAccess import Browser
from entitys import BrowserException


class BrowserController:
    browser: Browser

    def __init__(self, timeout: float = 30, **kwargs):
        """
        Initialize the BrowserController.
        :param kwargs: arguments passed to the Browser class.
        """
        try:
            self.goto_params = kwargs.pop('goto_params', {})
            logger.info('Started browser controller with browser args {!r} and goto args {!r}', kwargs,
                        self.goto_params)
            self.browser = Browser(timeout, **kwargs)
        except Exception as e:
            raise BrowserException('Failed to initialise BrowserController') from e

    def open(self, url: URL | str) -> None:
        """
        Open a browser url.
        :param url: URL to open
        """
        try:
            self.browser.open(url)
        except Exception as e:
            raise BrowserException('Failed to open url', url=url) from e

    def fill(self, field: str, value: str):
        """
        Fill a browser field with given value.
        :param field: Locator to element to fill
        :param value: Value to fill
        """
        try:
            self.browser.fill(field, value)
        except Exception as e:
            raise BrowserException(f'Failed to fill field {field!r} with value {value!r}',
                                   url=self.browser.url) from e

    def click(self, field: str):
        """
        Click in a browser element.
        :param field: Locator to element to click
        :param kwargs: Params passed to the Browser class.
        """
        try:
            self.browser.click(field)
        except Exception as e:
            raise BrowserException(f'Failed to click in the field {field!r}.', url=self.browser.url) \
                from e

    def get_all(self, field: str) -> list[WebElement]:
        """
        Get all elements of a browser based in locator.
        :param field: Locato to search
        :return: All elements of a browser based in locator.
        """
        try:
            return self.browser.get_all(field)
        except Exception as e:
            raise BrowserException(f'Failed to get all elements with field {field!r}.',
                                   url=self.browser.url) from e

    @staticmethod
    def get_attribute_from_sub_element(element: WebElement, field: str, attribute: str) -> str | None:
        """
        Get attribute of a sub element of a browser element.
        :param element: Base element
        :param field: Locator of the sub element
        :param attribute: Which attribute to get
        :return: Attribute of the sub element value or None if no sub element found
        """
        sub_element = element.find_elements(By.CSS_SELECTOR, field)
        if sub_element:
            return sub_element[0].get_attribute(attribute)
        return None

    @staticmethod
    def get_text_from_element(element: WebElement, field: str) -> str | None:
        """
        Get the text of a sub element of a browser element.
        :param element: Base element
        :param field: Locator of the sub element
        :return: Text of the sub element or None if no sub element found
        """
        sub_element = element.find_elements(By.CSS_SELECTOR, field)
        if sub_element:
            return sub_element[0].text
        return None

    def run_js(self, js):
        return self.browser.run_js(js)
