import re
from typing import Dict, List
from ofxtools import OFXTree
import pandas as pd
import os
from base import StatementEntry, EntriesReader


class OFXStatement(EntriesReader):
    def __init__(self, ofx_path):
        parser = OFXTree()
        try:
            self.tree = parser.parse(ofx_path)
            self.ofx = parser.convert()
        except Exception as error_msg:
            if str(error_msg).startswith("Elements out of order"):
                print("yes")
                fixed_file = self.reorder_ofx_fields(error_msg, ofx_path)
                self.tree = parser.parse(fixed_file)
                self.ofx = parser.convert()
            else:
                raise Exception(str(error_msg))

        self.start_date = self.ofx.statements[0].dtstart
        self.end_date = self.ofx.statements[0].dtend
        self.acc_id = self.ofx.statements[0].acctid

    def all_entries(self) -> List[StatementEntry]:
        entries = []
        for trans in self.ofx.statements[0].transactions:
            if trans.name:
                history = f"{trans.memo} - {trans.name}"
            else:
                history = trans.memo
            new_entry = StatementEntry(
                date=trans.dtposted.strftime(
                    "%d/%m/%Y"),
                history=history,
                value=trans.trnamt,
                bank_id=self.acc_id)
            entries.append(new_entry)
        return entries

    def reorder_ofx_fields(self, error_msg, ofx_path) -> str:
        pattern = r'(?<=STMTTRN, )\w+|(?<=occur before )\w+'
        second_field, first_field = re.findall(pattern, str(error_msg))

        lines = open(ofx_path, 'r').readlines()
        edited_file_path = ofx_path.replace(".ofx", "fixed .ofx")
        with open(edited_file_path, 'w') as edited:
            for i, line in enumerate(lines):
                if line.startswith(f"<{second_field}>") and lines[i - 1].startswith(f"<{first_field}>"):
                    continue
                elif line.startswith(f"<{first_field}>"):
                    if lines[i + 1].startswith(f"<{second_field}>"):
                        edited.write(lines[i + 1])
                    edited.write(line)
                else:
                    edited.write(line)
            edited.close()
        return edited_file_path


class MultipleOFXReader(EntriesReader):
    def __init__(self, folder_path):
        self.found_invalid_ofx = False
        self.ofx_files = [os.path.join(folder_path, file) for file in os.listdir(
            folder_path) if file.endswith(".ofx")]

    def all_entries(self) -> List[StatementEntry]:
        entries = []
        for ofx_file in self.ofx_files:
            try:
                data = OFXStatement(ofx_file)
            except Exception:
                print("Error reading OFX ", ofx_file)
            entries += data.all_entries()
        return entries

    def entries_by_account(self) -> Dict:
        entries = {}
        for ofx_file in self.ofx_files:
            try:
                data = OFXStatement(ofx_file)
            except Exception:
                print("Error reading OFX ", ofx_file)

            entries[data.acc_id] = data.all_entries()

        return entries

    def statements(self) -> List[OFXStatement]:
        statements = []
        for ofx_file in self.ofx_files:
            try:
                data = OFXStatement(ofx_file)
            except Exception:
                print("Error reading OFX ", ofx_file)

            statements.append(data)
        return statements
