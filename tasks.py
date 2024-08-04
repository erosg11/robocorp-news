from copy import deepcopy
from pathlib import Path
from typing import Type

from RPA.Excel.Files import Files as Excel
from robocorp import workitems, log
from robocorp.tasks import get_output_dir, task
from aiohttp import ClientTimeout

from Application import ApNewsApp, NewsApp, ImageDownloader
from entitys import BrowserException, ImageDownloadException

APPS: dict[str, Type[NewsApp]] = {
    'apnews.com': ApNewsApp,
}


@task
def producer():
    """Split Excel rows into multiple output Work Items for the next step."""
    output = get_output_dir() or Path("output")
    filename = "orders.xlsx"

    for item in workitems.inputs:
        path = item.get_file(filename, output / filename)

        excel = Excel()
        excel.open_workbook(path)
        rows = excel.read_worksheet_as_table(header=True)

        for row in rows:
            payload = {
                "Name": row["Name"],
                "Zip": row["Zip"],
                "Product": row["Item"],
            }
            workitems.outputs.create(payload)


@task
def consumer():
    """Process all the produced input Work Items from the previous step."""
    for item in workitems.inputs:
        try:
            name = item.payload["Name"]
            zipcode = item.payload["Zip"]
            product = item.payload["Product"]
            print(f"Processing order: {name}, {zipcode}, {product}")
            assert 1000 <= zipcode <= 9999, "Invalid ZIP code"
            item.done()
        except AssertionError as err:
            item.fail("BUSINESS", code="INVALID_ORDER", message=str(err))
        except KeyError as err:
            item.fail("APPLICATION", code="MISSING_FIELD", message=str(err))


@task
def do_search():
    log.info('Starting search')
    for item in workitems.inputs:
        try:
            app = APPS[item.payload["site"]](
                item.payload['since'], **item.payload['browser_config'])
            app.search(item.payload['search'])
            for result in app.get_news():
                log.debug('Got:', result)
                workitems.outputs.create(result.model_dump(mode='json'))
        except BrowserException as err:
            log.exception('Error while accessing', err.url)
            item.fail("BUSINESS", code="BROWSER", message=f'Error: {err!r}, URL: {err.url}')


@task
def download_image():
    log.info('Starting image download')
    output_dir = get_output_dir() or Path("output")
    output_dir /= 'imgs'
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
                log.info('Image not found to', repr(copy_item.get('title')))
                workitems.outputs.create(copy_item)
                continue
            try:
                workitems.outputs.create(copy_item, files=im.download_image(url))
            except ImageDownloadException as err:
                log.exception('Error while downloading Image', err.url)
                item.fail('BUSINESS', code='IMAGE_DOWNLOAD', message=f'Error: {err!r}, URL: {err.url!r} status code: {err.status}')
