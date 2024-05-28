import json
from datetime import datetime

def load_json(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def parse_date(date_str):
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Date '{date_str}' is not in a recognized format")
