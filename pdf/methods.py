import re

LOOK_FOR_NUMS = ["darf"]

def get_value(line):
    pattern = re.compile(
        r"[\d.,]+")
    match = pattern.search(line)
    if match is not None:
        return fix_value(match.group(0))


def fix_value(value):
    value = re.sub(r"\.", '', value)
    return re.sub(r",", ".", value)


def get_date(line):
    match = re.search(r"\d\d(/|-|\.)\d\d(/|-|\.)2\d\d\d", line)
    if match is not None:
        return match.group(0)

def date_at_beginning(line):
    match = re.search(r"^\d\d(/|-|\.)\d\d(/|-|\.)2\d\d\d", line)
    if match is not None:
        return match.group(0)

def get_info(line):
    if any(word in line for word in LOOK_FOR_NUMS):
        text = ''.join(i for i in line if i == " " or i.isalnum())
    else:
        text = ''.join(i for i in line if i == " " or i.isalpha())
    return re.sub(r'\b\w\b', '', text).strip()
