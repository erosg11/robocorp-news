from copy import deepcopy
from pathlib import Path
from typing import Type

import regex
from aiohttp import ClientTimeout
from robocorp import workitems
from loguru import logger
from robocorp.tasks import get_output_dir, task
from tenacity import retry, wait_exponential_jitter, stop_after_delay, stop_after_attempt

from Application import ApNewsApp, NewsApp, ImageDownloader, ExcelApp
from entitys import BrowserException, ImageDownloadException, NewsElement

APPS: dict[str, Type[NewsApp]] = {
    'apnews.com': ApNewsApp,
}


@task
def do_search():
    _do_search()


@logger.catch(reraise=True, message='Error while Doing Search')
def _do_search():
    """Task to search and create work items to the next task"""

    logger.info('Starting search')
    for item in workitems.inputs:
        try:
            app = APPS[item.payload["site"]](
                item.payload['since'], **item.payload['browser_config'])
            app.search(item.payload['search'], item.payload.get('categories'))
            for i, result in enumerate(app.get_news()):
                logger.debug('Got: {!r}', result)
                workitems.outputs.create(result.model_dump(mode='json', exclude_none=True))
                if i == 90:
                    logger.warning('Stoped to avoid WI limit')
                    break  # Limit of 100 WI
        except BrowserException as err:
            logger.exception('Error while accessing {!r}', err.url)
            item.fail("BUSINESS", code="BROWSER", message=f'Error: {err!r}, URL: {err.url}')


@task
def download_image():
    _download_image()


@logger.catch(reraise=True, message='Error while Downloading Image')
def _download_image():
    """Task to download an image from the URLs in the work items"""
    logger.info('Starting image download')
    output_dir = get_output_dir() or Path("output")
    output_dir.mkdir(exist_ok=True, parents=True)
    with ImageDownloader(output_dir=output_dir,
                         headers={'user-agent':
                                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 '
                                      'OPR/68.0.3618.197'},
                         timeout=ClientTimeout(20),
                         ) as im:
        for item in workitems.inputs:
            copy_item = deepcopy(item.payload)
            url = copy_item.get('picture_url')
            if url is None:
                logger.info('Image not found to {!r}', copy_item.get('title'))
                workitems.outputs.create(copy_item)
                continue
            try:
                workitems.outputs.create(copy_item, files=im.download_image(url))
            except ImageDownloadException as err:
                logger.exception('Error while downloading Image {!r}', err.url)
                item.fail('BUSINESS', code='IMAGE_DOWNLOAD',
                          message=f'Error: {err!r}, URL: {err.url!r} status code: {err.status}')


@task
def excel_writer():
    _excel_writer()


@logger.catch(reraise=True, message='Error while writing Excel')
def _excel_writer():
    """Task to read data from work items and save in the excel file"""
    logger.info('Starting excel writer')
    output_dir = get_output_dir() or Path("output")
    output_dir.mkdir(exist_ok=True, parents=True)
    excel_filename = output_dir / 'data.xlsx'
    with ExcelApp(excel_filename) as excel:
        for item in workitems.inputs:
            logger.debug('Get the item {!r}', item)
            element = NewsElement(**item.payload)
            file = item.files
            if file:
                element.file = item.get_file(file[0], output_dir / file[0])
                element.filename = element.file.name
            else:
                logger.info('No image found for the item {!r}', element)
                element.file = ''
                element.filename = ''
            element.count_matches = f"{element.title or ''}\n{element.description or ''}".upper().count(
                element.search_phrase.upper()
            )
            element.has_dollars = 'TRUE' if bool(regex.search(
                r'(?P<dollar_sign>\$\s*)?(?:\d+,)*\d+(?:\.\d*)?(?(dollar_sign)|\s+(?:dollars?|USD))',
                f'{element.title or ""}\n{element.description or ""}', flags=regex.IGNORECASE
            )) else 'FALSE'
            excel.append_row(element.model_dump(exclude={'search_phrase'}, mode='json'))
