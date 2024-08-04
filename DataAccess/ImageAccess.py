from aiohttp import ClientSession
import asyncio
from pathlib import Path
from uuid import uuid4
from contextlib import AsyncExitStack

from yarl import URL


CHUNK_SIZE = 10 * 2 ** 20


class ImageAccess:
    def __init__(self, **kwargs):
        self.loop = asyncio.get_event_loop()
        self.client = self.loop.run_until_complete(self._create_session(**kwargs))

    @staticmethod
    async def _create_session(**kwargs):
        return ClientSession(**kwargs)

    def __enter__(self):
        self.client = self.loop.run_until_complete(self.client.__aenter__())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop.run_until_complete(self.client.__aexit__(exc_type, exc_val, exc_tb))
        self.loop.close()

    def download_image(self, url: URL | str, base_path: Path):
        return self.loop.run_until_complete(self._download_image(url, base_path))

    async def _download_image(self, url: URL | str, base_path: Path):
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


class RequestError(Exception):
    def __init__(self, message, status: int, url: URL):
        super().__init__(message)
        self.status = status
        self.url = url
