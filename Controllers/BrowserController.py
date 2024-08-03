from DataAccess import Browser
from entitys import BrowserException
from functools import partial


class BrowserController:
    browser: Browser

    def __init__(self, **kwargs):
        try:
            self.goto_params = kwargs.pop('goto_params', {})
            self.browser = Browser(**kwargs)
            self.open_url = partial(self.browser.open, **self.goto_params)
        except Exception as e:
            raise BrowserException('Failed to initialise BrowserController') from e

    def open(self, url):
        try:
            self.open_url(url)
        except Exception as e:
            raise BrowserException('Failed to open url', url=url) from e

    def fill(self, field, value):
        try:
            self.browser.fill(field, value)
        except Exception as e:
            raise BrowserException(f'Failed to fill field {field!r} with value {value!r}',
                                   url=self.browser.page.url) from e

    def click(self, field, **kwargs):
        try:
            self.browser.click(field, **kwargs)
        except Exception as e:
            raise BrowserException(f'Failed to click in the field {field!r}.', url=self.browser.page.url) \
                from e

    def get_all(self, field):
        try:
            return self.browser.get_all(field)
        except Exception as e:
            raise BrowserException(f'Failed to get all elements with field {field!r}.',
                                   url=self.browser.page.url) from e

    @staticmethod
    def get_attribute_from_sub_element(element, field, attribute):
        elemen = element.query_selector(field)
        if elemen is not None:
            return elemen.get_attribute(attribute)
        return None

    @staticmethod
    def get_text_from_element(element, field):
        elemen = element.query_selector(field)
        if elemen is not None:
            return elemen.inner_text()
        return None
