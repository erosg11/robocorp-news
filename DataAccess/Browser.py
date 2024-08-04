from robocorp import browser
from playwright.sync_api import Page


class Browser:
    _page: Page | None = None

    def __init__(self, **kwargs):
        browser.configure(
            screenshot="only-on-failure",
            headless=False,
            slowmo=100,
            **kwargs,
        )
        self._page = browser.page()

    def open(self, url, **kwargs) -> Page:
        self._page.goto(url, **kwargs)
        return self._page

    def fill(self, field, value):
        self._page.fill(field, value)

    def click(self, field, **kwargs):
        self._page.click(field, **kwargs)

    def get_all(self, field):
        return self._page.query_selector_all(field)

    @property
    def url(self):
        return self._page.url

