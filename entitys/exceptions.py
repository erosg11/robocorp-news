from yarl import URL
from typing import Union


class BrowserException(Exception):
    url: URL

    def __init__(self, message: str, url: Union[URL, str, None] = None):
        super().__init__(message)
        self.url = URL(url)
