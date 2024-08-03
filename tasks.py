from datetime import date
from pathlib import Path

from robocorp import workitems
from robocorp.tasks import get_output_dir, task
from RPA.Excel.Files import Files as Excel
from entitys import BrowserException
from Application import ApNewsApp, NewsApp
from typing import Type

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
    for item in workitems.inputs:
        try:
            app = APPS[item.payload["site"]](
                item.payload['since'], **item.payload['browser_config'])
            app.search(item.payload['search'])
            for result in app.get_news():
                workitems.outputs.create(result.model_dump(mode='json'))
        except BrowserException as err:
            item.fail("BUSINESS", code="BROWSER", message=f'Error: {err!r}, URL: {err.url}')
