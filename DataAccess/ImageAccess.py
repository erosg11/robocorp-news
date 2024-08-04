"""Data Access layer to the image donwload"""

from aiohttp import ClientSession
import asyncio
from pathlib import Path
from uuid import uuid4
from contextlib import AsyncExitStack

from yarl import URL

from entitys import RequestError

CHUNK_SIZE = 10 * 2 ** 20


class ImageAccess:
    """
    Class in the data access layer to download images.
    """
    def __init__(self, **kwargs):
        """
        Initialize the data access layer for image download.
        :param kwargs: arguments passed to the constructor of the aiohttp.ClientSession.
        """
        self.loop = asyncio.get_event_loop()
        self.client = self.loop.run_until_complete(self._create_session(**kwargs))

    @staticmethod
    async def _create_session(**kwargs) -> ClientSession:
        """Method that creates a new aiohttp session."""
        return ClientSession(**kwargs)

    def __enter__(self) -> "ImageAccess":
        """Start the aiohttp session."""
        self.client = self.loop.run_until_complete(self.client.__aenter__())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the aiohttp session and the loop."""
        self.loop.run_until_complete(self.client.__aexit__(exc_type, exc_val, exc_tb))
        self.loop.close()

    def download_image(self, url: URL | str, base_path: Path) -> Path:
        """Method that downloads the image from the url."""
        return self.loop.run_until_complete(self._download_image(url, base_path))

    async def _download_image(self, url: URL | str, base_path: Path) -> Path:
        """Method that downloads the image from the url."""
        out_file = base_path / f'{uuid4()}.jpg'
        async with AsyncExitStack() as stack:
            fp = stack.enter_context(out_file.open('wb'))
            response = await stack.enter_async_context(self.client.get(url))
            if response.status >= 400:
                raise RequestError(
                    f'Error downloading image, truncated response: {await response.content.read(1024)}',
                    status=response.status, url=url)
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                fp.write(chunk)
        return out_file

