from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import Workbook
import os

from config import COLUMNS, SHEET_NAME, TOTAL_EARNINGS

class ExcelWriter:

    def __enter__(self):
        self.wb = Workbook()
        self.ws: Worksheet = self.wb.active
        if not self.ws:
            raise FileExistsError("Can not found work sheet")
        self.ws.title = SHEET_NAME 

        if not os.path.exists('data'):
            os.makedirs('data')

        self.ws.append(*COLUMNS)
        return self

    def write_general_data(self, write_data) -> None:
        self.ws.append(write_data)


    def write_total_data(self) -> None:
        self.ws.append([])
        self.ws.append(['Имя', 'З/п', 'Смены'])
        for name in TOTAL_EARNINGS:
            write_data = [
                name,
                TOTAL_EARNINGS[name]['total_earnings'],
                TOTAL_EARNINGS[name]['shift'],
            ]
            self.ws.append(write_data)

    def __exit__(self, exc_type, exc_value, traceback):
        filepath = os.path.join('data', f"{SHEET_NAME}.xlsx")
        self.wb.save(filepath)

        if exc_type:
            print(f"An exception occurred: {exc_value}")
        return True  # Suppress exceptions if needed
