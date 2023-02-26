
import re
from methods import fix_value
from pdfreader import PDFreader
from methods import date_at_beginning, get_info
from decimal import Decimal
import sys
import os
# Add the parent directory of the current script to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from models import EntriesReader, StatementEntry

START_KW = "saldo anterior"
END_KW = "s a l d o"
ACC_ID = r"conta corrente (\d+\-?\d?)"


class BBParser(EntriesReader):
    def __init__(self, pdf_path):
        reader = PDFreader()
        self.raw_txt = reader.read(pdf_path).lower()
        self.acc_id = None

    def all_entries(self):
        self.preprocess()
        entries = []
        current_entry = None
        has_entry = False

        for i, line in enumerate(self.lines):
            date = date_at_beginning(line)
            if date:
                value = self.get_bb_value(line)
                # rare case fix
                if not value:
                    value = self.get_bb_value(self.lines[i + 1])
                    
                if current_entry and self.is_valid_entry(current_entry):
                    entries.append(current_entry)
                current_entry = StatementEntry(date=date, history=get_info(
                    line), value=value, bank_id="bb")
                has_entry = True
            else:
                if has_entry:
                    current_entry.history = ' '.join(
                        [current_entry.history, get_info(line)])
                else:
                    current_entry = StatementEntry(
                        date=date_at_beginning(line), history=get_info(line), value=self.get_bb_value(line))
                    has_entry = True

        if current_entry and self.is_valid_entry(current_entry):
            entries.append(current_entry)
        
        return entries

    def is_valid_entry(self, entry:StatementEntry):
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
        for i , line in enumerate(all_lines):
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

    def get_acc_id(self):
        ptr = ACC_ID
        match = re.search(ptr, self.raw_txt)
        if match is not None:
            self.acc_id = match.group(1)

    def get_bb_value(self, line):
        pattern = re.compile(
            r"\s([\d.,]+) ([dc])(?:\s|$|\d)")
        match = pattern.search(line)
        if match is not None:
            val = match.group(1)
            is_payment = match.group(2) == "d"
            if is_payment:
                return float(fix_value(val).strip()).__neg__()
            else:
                return float(fix_value(val).strip())

    
    def clean_line(self, line):
        pattern = r"\d{1,3}(\.\d{3})+"
        line = re.sub(pattern, "", line, count=1)
        return line.strip()    
