import ofxtools
from ofxtools import OFXTree
import pandas as pd
import os
from models import StatementEntry, EntriesReader


class OFXReader(EntriesReader):
    def __init__(self, folder_path):
        self.found_invalid_ofx = False
        self.ofx_files = [os.path.join(folder_path, file) for file in os.listdir(
            folder_path) if file.endswith(".ofx")]

    def all_entries(self):
        entries = []
        for ofx_file in self.ofx_files:
            try:
                data = OFXStatement(ofx_file)
            except Exception:
                print("Error reading OFX ", ofx_file)
            entries += data.all_entries()
        return entries

    def entries_by_account(self):
        entries = {}
        for ofx_file in self.ofx_files:
            try:
                data = OFXStatement(ofx_file)
            except Exception:
                print("Error reading OFX ", ofx_file)

            entries[data.acc_id] = data.all_entries()

        return entries

    def statements(self):
        statements = []
        for ofx_file in self.ofx_files:
            try:
                data = OFXStatement(ofx_file)
            except Exception:
                print("Error reading OFX ", ofx_file)

            statements.append(data)
        return statements


class OFXStatement(EntriesReader):
    def __init__(self, ofx_path):
        parser = OFXTree()
        self.tree = parser.parse(ofx_path)
        self.ofx = parser.convert()
        self.start_date = self.ofx.statements[0].dtstart
        self.end_date = self.ofx.statements[0].dtend
        self.acc_id = self.ofx.statements[0].acctid

    def all_entries(self):
        entries = []
        for trans in self.ofx.statements[0].transactions:
            new_entry = StatementEntry(
                date=trans.dtposted.strftime(
                    "%d/%m/%Y"),
                history=trans.memo,
                value=trans.trnamt,
                bank_id=self.acc_id)
            entries.append(new_entry)
        return entries
