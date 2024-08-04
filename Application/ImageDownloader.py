from pathlib import Path

from robocorp import log

from Controllers import ImageController


class ImageDownloader:
    def __init__(self, output_dir: Path, **kwargs):
        self.ic = ImageController(output_dir, **kwargs)

    def download_image(self, url):
        log.debug('Downloading image:', url)
        return self.ic.download_image(url)

    def __enter__(self):
        self.ic.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ic.__exit__(exc_type, exc_val, exc_tb)
