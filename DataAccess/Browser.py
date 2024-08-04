"""Browser data access layer"""

from robocorp import browser
from playwright.sync_api import Page, JSHandle
from yarl import URL


class Browser:
    """Browser data access layer"""
    _page: Page | None = None

    def __init__(self, **kwargs):
        """Initialize the Browser object."""
        browser.configure(
            **kwargs,
        )
        self._page = browser.page()

    def open(self, url: URL | str, **kwargs) -> Page:
        """
        Open a browser page.
        :param url: URL to open.
        :param kwargs: arguments passed to Page.goto().
        :return: The browser page.
        """
        self._page.goto(url, **kwargs)
        return self._page

    def fill(self, field: str, value: str):
        """
        Fill a page element with a given value.
        :param field: Locator to the element to fill
        :param value: Value to fill.
        """
        self._page.fill(field, value)

    def click(self, field: str, **kwargs):
        """
        Click an element.
        :param field: Locator to the element to click.
        :param kwargs: Arguments passed to Page.click().
        """
        self._page.click(field, **kwargs)

    def get_all(self, field: str) -> list[JSHandle]:
        """
        Get all elements of a page that match the given locator.
        :param field: Locator to search for.
        """
        return self._page.query_selector_all(field)

    @property
    def url(self) -> str:
        """Get the URL of the current page."""
        return self._page.url

