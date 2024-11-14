import re

API_TOKEN = ''

SHEET_NAME = "Рассчет_зарплаты"

BASE_RATE = 1300
TOTAL_EARNINGS = {}

COLUMNS = ['Дата', 'День/Ночь', 'Имя', 'Касса', 'Нал', 'Карта', 'Ставка','Процент', 'Итого'],
PATTERN = re.compile(r'(?P<time>\d{1,2}:\d{1,2}\s*-\s*\d{1,2}:\d{1,2})\s*\n(?P<name>\w+)\s*\n(?P<date>\d{1,2}\.\d{1,2})\s*\nКасса:?\s*(?P<kassa>\d+)\s*\nНал:?\s*(?P<cash>\d+)\s*\nКарта:?\s*(?P<card>\d+)\s*\nДенег в кассе:?\s*(?P<money>[\d\s]+)(?:\s*\(.*\))?\s*\nПроцент:?\s*(?P<percent>\d+)\s*')
