"""Controller layer to Browser module."""
from playwright.sync_api import JSHandle
from loguru import logger
from yarl import URL

from DataAccess import Browser
from entitys import BrowserException
from functools import partial


class BrowserController:
    browser: Browser

    def __init__(self, **kwargs):
        """
        Initialize the BrowserController.
        :param kwargs: arguments passed to the Browser class.
        """
        try:
            self.goto_params = kwargs.pop('goto_params', {})
            logger.info('Started browser controller with browser args {!r} and goto args {!r}', kwargs,
                        self.goto_params)
            self.browser = Browser(**kwargs)
            self.open_url = partial(self.browser.open, **self.goto_params)
        except Exception as e:
            raise BrowserException('Failed to initialise BrowserController') from e

    def open(self, url: URL | str) -> None:
        """
        Open a browser url.
        :param url: URL to open
        """
        try:
            self.open_url(url)
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

    def click(self, field: str, **kwargs):
        """
        Click in a browser element.
        :param field: Locator to element to click
        :param kwargs: Params passed to the Browser class.
        """
        try:
            self.browser.click(field, **kwargs)
        except Exception as e:
            raise BrowserException(f'Failed to click in the field {field!r}.', url=self.browser.url) \
                from e

    def get_all(self, field: str) -> list[JSHandle]:
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
    def get_attribute_from_sub_element(element: JSHandle, field: str, attribute: str) -> str | None:
        """
        Get attribute of a sub element of a browser element.
        :param element: Base element
        :param field: Locator of the sub element
        :param attribute: Which attribute to get
        :return: Attribute of the sub element value or None if no sub element found
        """
        sub_element = element.query_selector(field)
        if sub_element is not None:
            return sub_element.get_attribute(attribute)
        return None

    @staticmethod
    def get_text_from_element(element: JSHandle, field: str) -> str | None:
        """
        Get the text of a sub element of a browser element.
        :param element: Base element
        :param field: Locator of the sub element
        :return: Text of the sub element or None if no sub element found
        """
        sub_element = element.query_selector(field)
        if sub_element is not None:
            return sub_element.inner_text()
        return None
