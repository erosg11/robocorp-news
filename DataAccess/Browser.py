"""Browser data access layer"""

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement
from yarl import URL
from datetime import timedelta


class Browser:
    """Browser data access layer"""

    # _page: Page | None = None

    def __init__(self, timeout: float = 30, **kwargs):
        """Initialize the Browser object."""
        headless = kwargs.pop('headless', False)
        self._lib = Selenium(**kwargs)
        self._lib.open_available_browser(options={"arguments": ['--headless'] if headless else []})
        self._lib.set_selenium_timeout(timedelta(seconds=timeout))

    def open(self, url: URL | str):
        """
        Open a browser page.
        :param url: URL to open.
        :return: The browser page.
        """
        self._lib.go_to(url)

    def fill(self, field: str, value: str):
        """
        Fill a page element with a given value.
        :param field: Locator to the element to fill
        :param value: Value to fill.
        """
        self._lib.input_text(field, value)

    def click(self, field: str):
        """
        Click an element.
        :param field: Locator to the element to click.
        """
        self._lib.click_element_if_visible(field)

    def get_all(self, field: str) -> list[WebElement]:
        """
        Get all elements of a page that match the given locator.
        :param field: Locator to search for.
        """
        return self._lib.find_elements(field)

    @property
    def url(self) -> str:
        """Get the URL of the current page."""
        return self._lib.get_location()
