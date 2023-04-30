
import sys
import os
# Add the parent directory of the current script to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from ..base import EntriesReader, StatementEntry

import re
from typing import List
from .pdfreader import PDFreader
from .methods import date_at_beginning, get_info, fix_value
from decimal import Decimal

START_KW = "saldo anterior"
END_KW = "s a l d o"
ACC_ID = r"conta corrente (\d+\-?\d?)"


class BBpdfParser(EntriesReader):
    def __init__(self, pdf_path):
        reader = PDFreader()
        self.raw_txt = reader.read(pdf_path).lower()
        self.acc_id = None
        self.preprocess()
        
    def all_entries(self) -> List[StatementEntry]:
        entries = []
        current_entry = None

        for i, line in enumerate(self.lines):
            date = date_at_beginning(line)
            if date:
                value = self.get_bb_value(line)
                # rare case fix
                if not value and not self.lines[i + 1].startswith(r"\d\d/\d\d"):
                    value = self.get_bb_value(self.lines[i + 1])

                if current_entry and self.is_valid_entry(current_entry):
                    entries.append(current_entry)
                current_entry = StatementEntry(date=date, history=get_info(
                    line), value=value, bank_id="bb")
            else:
                if current_entry:
                    current_entry.history = ' '.join(
                        [current_entry.history, get_info(line)])
                else:
                    id = self.get_acc_id()
                    current_entry = StatementEntry(
                        date=date_at_beginning(line), history=get_info(line), value=self.get_bb_value(line), bank_id=id if id else "bb")

        if current_entry and self.is_valid_entry(current_entry):
            entries.append(current_entry)

        return entries


    def is_valid_entry(self, entry: StatementEntry) -> bool:
        for val in vars(entry).values():
            if val is None:
                return False
        return True

    def preprocess(self):
        self.get_acc_id()
        self.read_lines()

    def read_lines(self):
        all_lines = self.raw_txt.split("\n")
        valid_lines = []
        within_range = False
        for line in all_lines:
            line = self.clean_line(line)
            if not within_range:
                if START_KW in line:
                    within_range = True
                continue

            if END_KW in line:
                break

            if len(line) > 1:
                valid_lines.append(line)
            else:
                valid_lines[-1] = valid_lines[-1] + " " + line

        self.lines = valid_lines

    def get_acc_id(self) -> str | None:
        ptr = ACC_ID
        match = re.search(ptr, self.raw_txt)
        if match is not None:
            self.acc_id = match.group(1)
        return None

    def get_bb_value(self, line: str) -> Decimal | None:
        pattern = re.compile(
            r"\s([\d.,]+) ([dc])(?:\s|$|\d)")
        match = pattern.search(line)
        if match is not None:
            val = match.group(1)
            is_payment = match.group(2) == "d"
            if is_payment:
                return Decimal(self.fix_bb_value(val).strip()).__neg__()
            else:
                return Decimal(self.fix_bb_value(val).strip())
        return None

    def clean_line(self, line: str) -> str:
        pattern = r"\d{1,3}(\.\d{3})+"
        line = re.sub(pattern, "", line, count=1)
        return line.strip()

    def fix_bb_value(self, value: str) -> str:
        # removing numbers to the left that don't contain a dot
        fixed_value = value[-3:]
        index = len(value) - 4
        digit_count = 0
        while index >= 0:
            if digit_count == 3:
                if value[index] == ".":
                    fixed_value = value[index] + fixed_value
                    digit_count = 0
                else:
                    break
            else:
                fixed_value = value[index] + fixed_value
                digit_count += 1
            index -= 1
        # replacing signs
        fixed_value = re.sub(r"\.", '', fixed_value)
        fixed_value = re.sub(r",", ".", fixed_value)
        return fixed_value