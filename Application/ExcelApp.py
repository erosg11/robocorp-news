from pathlib import Path

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from entitys import ExcelException


class ExcelApp:
    """Application class for ExcelApp"""
    filename: Path
    _excel: Workbook | None = None
    _worksheet_name: str = 'Sheet1'

    def __init__(self, filename: Path, worksheet: str = 'Sheet1'):
        """
        ExcelApp constructor.
        :param filename: Excel file path.
        :param worksheet: Worksheet name.
        """
        self.filename = filename
        self._worksheet_name = worksheet
        self._worksheet = None  # type: Worksheet | None
        self._data = []
        self.append_data = self._data.append
        self._headers = None

    def __enter__(self):
        """Starter to the excel file, MUST BE CALLED"""
        self._excel = Workbook()
        self._worksheet = self._excel.create_sheet(self._worksheet_name)
        self._excel.active = self._worksheet
        self.append_row = self._append_first_row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Write the data in the excel file, save and close it."""
        self._excel.close()

    def append_row(self, row: dict):
        """Add the row to the buffer to be written to the excel file"""
        raise ExcelException('Cannot append row to excel file not initialized')

    def _append_first_row(self, row: dict):
        self._headers = list(row.keys())
        self.append_row = self._append_row
        self._worksheet.append(self._headers)
        self.append_row(row)

    def _append_row(self, row: dict):
        self._worksheet.append([row[k] for k in self._headers])
        self._excel.save(self.filename)
