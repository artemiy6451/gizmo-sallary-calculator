from datetime import datetime

def extract_date_time(entry):
    try: 
        lines = entry.split('\n')
        date_str = lines[2].strip()
        date = datetime.strptime(date_str, '%d.%m')
        time_range = lines[0].split('-')[0].strip()
        time_start = datetime.strptime(time_range, '%H:%M').time()
        return date, time_start
    except Exception:
        return datetime.now(), ""
