"""Application that download images"""

from pathlib import Path

from loguru import logger

from Controllers import ImageController


class ImageDownloader:
    """Application that download images"""
    def __init__(self, output_dir: Path, **kwargs):
        """
        Initialize the ImageDownloader object.
        :param output_dir: Directory where images will be downloaded.
        :param kwargs: Arguments to be passed to the aiohttp.ClientSession.
        """
        self.ic = ImageController(output_dir, **kwargs)

    def download_image(self, url) -> Path:
        """
        Download an image from the given URL.
        :param url: URL to download.
        :return: Downloaded image path.
        """
        logger.debug('Downloading image: {!r}', url)
        return self.ic.download_image(url)

    def __enter__(self):
        """Start the image downloader."""
        self.ic.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the image downloader."""
        self.ic.__exit__(exc_type, exc_val, exc_tb)
