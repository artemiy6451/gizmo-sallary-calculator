from config import BASE_RATE, PATTERN, TOTAL_EARNINGS
from datetime import datetime


def calculate_salary(data: str) -> list | None:
    match = PATTERN.search(data)
    if match is None:
        print(f"Can not fond patern: \n{data}\n")
        return None

    parced_data = match.groupdict()
    time_range = parced_data["time"].split('-')[0].strip()
    time_start = datetime.strptime(time_range, '%H:%M').time()
    if time_start.hour > 14:
        time = "Ночь"
    else:
        time = "День"

    name = parced_data["name"]
    earnings = BASE_RATE + int(parced_data['percent'])

    if name in TOTAL_EARNINGS:
        TOTAL_EARNINGS[name]['total_earnings'] += earnings
        TOTAL_EARNINGS[name]['shift'] += 1
    else:
        TOTAL_EARNINGS[name] = {'total_earnings': earnings, 'shift': 1}

    return [
        parced_data['date'],
        time,
        parced_data["name"],
        int(parced_data["kassa"]),
        parced_data["cash"],
        parced_data["card"],
        BASE_RATE,
        int(parced_data["percent"]),
        BASE_RATE + int(parced_data["percent"])
    ]


def clear_data():
    TOTAL_EARNINGS.clear()
