from pathlib import Path

from entitys import ImageDownloadException
from DataAccess import ImageAccess, RequestError


class ImageController:
    def __init__(self, output_dir: Path, **kwargs):
        self.ia = ImageAccess(**kwargs)
        self.output_dir = output_dir

    def download_image(self, url):
        try:
            return self.ia.download_image(url, self.output_dir)
        except RequestError as e:
            raise ImageDownloadException('Error while downloading image', url=e.url, status=e.status) from e
        except Exception as e:
            raise ImageDownloadException('Error while downloading image', url=url) from e

    def __enter__(self):
        self.ia = self.ia.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ia.__exit__(exc_type, exc_val, exc_tb)
