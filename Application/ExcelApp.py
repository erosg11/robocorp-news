from pathlib import Path

from RPA.Excel.Files import Files as Excel


class ExcelApp:
    """Application class for ExcelApp"""
    filename: Path
    _excel: Excel | None = None
    _worksheet_name: str = 'Sheet1'

    def __init__(self, filename: Path, worksheet: str = 'Sheet1'):
        """
        ExcelApp constructor.
        :param filename: Excel file path.
        :param worksheet: Worksheet name.
        """
        self.filename = filename
        self._worksheet_name = worksheet
        self._data = []
        self.append_data = self._data.append

    def __enter__(self):
        """Starter to the excel file, MUST BE CALLED"""
        self._excel = Excel()
        self._excel.create_workbook(str(self.filename))
        self._excel.save_workbook()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Write the data in the excel file, save and close it."""
        if exc_type is None and self._data:
            self._excel.create_worksheet(self._worksheet_name, self._data, header=True)
            self._excel.save_workbook()
        self._excel.close_workbook()

    def append_row(self, row):
        """Add the row to the buffer to be written to the excel file"""
        self.append_data(row)
