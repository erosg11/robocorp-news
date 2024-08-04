"""Controller layer to image download"""


from pathlib import Path

from yarl import URL

from entitys import ImageDownloadException
from DataAccess import ImageAccess
from entitys import RequestError


class ImageController:
    """Controller layer to image download"""
    def __init__(self, output_dir: Path, **kwargs):
        """Initialise the ImageController"""
        self.ia = ImageAccess(**kwargs)
        self.output_dir = output_dir

    def download_image(self, url: URL | str) -> Path:
        """Download image from url"""
        try:
            return self.ia.download_image(url, self.output_dir)
        except RequestError as e:
            raise ImageDownloadException('Error while downloading image', url=e.url, status=e.status) from e
        except Exception as e:
            raise ImageDownloadException('Error while downloading image', url=url) from e

    def __enter__(self) -> 'ImageController':
        """Enter in ImageController"""
        self.ia = self.ia.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit ImageController"""
        self.ia.__exit__(exc_type, exc_val, exc_tb)
