import re
from fuzzywuzzy import fuzz


def strings_similar(string1, string2, min_likeness=90):
    distance = fuzz.ratio(string1.lower(), string2.lower())
    return distance >= min_likeness


LOOK_FOR_NUMS = ["darf"]


def get_value(line : str) -> str | None:
    pattern = re.compile(
        r"[\d.,]+")
    match = pattern.search(line)
    if match is not None:
        return fix_value(match.group(0))
    return None

def fix_value(value : str) -> str:
    value = re.sub(r"\.", '', value)
    return re.sub(r",", ".", value)


def get_date(line : str) -> str | None:
    match = re.search(r"\d\d(/|-|\.)\d\d(/|-|\.)2\d\d\d", line)
    if match is not None:
        return match.group(0)
    return None


def date_at_beginning(line : str) -> str | None:
    match = re.search(r"^\d\d(/|-|\.)\d\d(/|-|\.)2\d\d\d", line)
    if match is not None:
        return match.group(0)
    return None


def get_info(line : str):
    if any(word in line for word in LOOK_FOR_NUMS):
        text = ''.join(i for i in line if i == " " or i.isalnum())
    else:
        text = ''.join(i for i in line if i == " " or i.isalpha())
    return re.sub(r'\b\w\b', '', text).strip()
