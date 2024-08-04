from yarl import URL


class BrowserException(Exception):
    """Exception raised when a browser exception occurs."""
    url: URL

    def __init__(self, message: str, url: URL | str | None = None):
        super().__init__(message)
        self.url = URL(url)


class ImageDownloadException(BrowserException):
    """Exception raised when an image download exception occurs."""
    def __init__(self, message: str, url: URL | str | None = None, status: int | None = None):
        super().__init__(message, url)
        self.status = status


class RequestError(Exception):
    """Exception raised when a request exception occurs."""
    def __init__(self, message, status: int, url: URL):
        super().__init__(message)
        self.status = status
        self.url = url


class ExcelException(Exception):
    """Exception raised when an excel exception occurs."""
    def __init__(self, message: str, row: int | None = None):
        super().__init__(message)
        self.row = row
