from yarl import URL
from typing import Union


class BrowserException(Exception):
    url: URL

    def __init__(self, message: str, url: URL | str | None = None):
        super().__init__(message)
        self.url = URL(url)


class ImageDownloadException(BrowserException):
    def __init__(self, message: str, url: URL | str | None = None, status: int | None = None):
        super().__init__(message, url)
        self.status = status
