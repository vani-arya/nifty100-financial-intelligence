import re


def normalize_ticker(ticker):
    if ticker is None:
        return None

    return str(ticker).strip().upper()


def normalize_year(year_value):
    if year_value is None:
        return None

    year_str = str(year_value).strip()

    match = re.search(r"(20\d{2})", year_str)

    if match:
        return int(match.group(1))

    match = re.search(r"-(\d{2})$", year_str)

    if match:
        return int("20" + match.group(1))

    raise ValueError(f"Cannot parse year: {year_value}")