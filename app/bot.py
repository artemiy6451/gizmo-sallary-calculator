import re
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import Workbook
import os

FILE_NAME = "data/fsdf.txt"
SHEET_NAME = "Рассчет_зарплаты"
BASE_RATE = 1300
TOTAL_EARNINGS = {}
COLUMNS = ['Дата', 'День/Ночь', 'Имя', 'Касса', 'Ставка','Процент', 'Итого'],
PATTERN = re.compile(r'(?P<time>[\d:]+-[\d:]+)\n(?P<name>\w+)\n(?P<date>\d+\.\d+)\nКасса: (?P<kassa>\d+)\nНал: (?P<cash>\d+)\nКарта: (?P<card>\d+)\nДенег в кассе: (?P<money>\d+)\nПроцент: (?P<percent>\d+)')


def read_file(name: str) -> str:

    with open(name, 'r', encoding='utf-8') as file:
        content = file.read()

    if content is None:
        exit('File can not read or open')

    return content


def create_workbook(name: str) -> tuple[Workbook, Worksheet]:
    wb = Workbook()
    ws = wb.active
    if not ws:
        raise FileExistsError("Can not found work sheet")
    ws.title = name 

    if not os.path.exists('data'):
        os.makedirs('data')

    ws.append(*COLUMNS)

    return wb, ws

def write_general_data(ws: Worksheet) -> None:
    content = read_file(FILE_NAME)
    blocks = content.strip().split('\n\n')
    for block in blocks:
        match = PATTERN.search(block)
        if match is None:
            print(f"Can not fond patern: \n{block}\n")
            continue 

        data = match.groupdict()
        if data["time"].startswith("1") or data["time"].startswith("2"):
            time = "Ночь"
        else:
            time = "День"

        write_data = [
            data['date'],
            time,
            data["name"],
            int(data["kassa"]),
            BASE_RATE,
            int(data["percent"]),
            BASE_RATE + int(data["percent"])
        ]

        ws.append(write_data)

        name = data['name']
        data['percent'] = int(data['percent'])

        earnings = BASE_RATE + data['percent']
        data['earnings'] = earnings

        # Добавление заработка к общему результату для каждого человека
        if name in TOTAL_EARNINGS:
            TOTAL_EARNINGS[name]['total_earnings'] += earnings
            TOTAL_EARNINGS[name]['shift'] += 1
        else:
            TOTAL_EARNINGS[name] = {'total_earnings': earnings, 'shift': 1}

def color_cell(ws: Worksheet):
    pass

def write_total_data(ws: Worksheet) -> None:
    ws.append([])
    ws.append(['Имя', 'З/п', 'Смены'])
    for name in TOTAL_EARNINGS:
        write_data = [
            name,
            TOTAL_EARNINGS[name]['total_earnings'],
            TOTAL_EARNINGS[name]['shift'],
        ]
        ws.append(write_data)


def save_workbook(wb: Workbook, name: str) -> None:
    filepath = os.path.join('data', f"{name}.xlsx")
    wb.save(filepath)


if __name__ == "__main__":
    wb, ws = create_workbook(SHEET_NAME) 
    write_general_data(ws)
    write_total_data(ws)
    save_workbook(wb, SHEET_NAME)
