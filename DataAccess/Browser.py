from robocorp import browser
from playwright.sync_api import Page


class Browser:
    page: Page | None = None

    def __init__(self, **kwargs):
        browser.configure(
            screenshot="only-on-failure",
            headless=False,
            slowmo=100,
            **kwargs,
        )
        self.page = browser.page()

    def open(self, url, **kwargs) -> Page:
        self.page.goto(url, **kwargs)
        return self.page

    def fill(self, field, value):
        self.page.fill(field, value)

    def click(self, field, **kwargs):
        self.page.click(field, **kwargs)

    def get_all(self, field):
        element = self.page.query_selector_all(field)
        if element is None:
            raise KeyError(f'Element {field} not found')
        return element

