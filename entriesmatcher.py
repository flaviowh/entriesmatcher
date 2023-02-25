
from ofxreader import OFXReader
from sheetreader import SheetReader
from models import *


class EntriesMatcher(EntriesReader):
    def __init__(self, ofxreader: EntriesReader, sheetreader: SheetReader):
        self.ofxreader = ofxreader
        self.sheetreader = sheetreader

    def all_entries(self):
        return self.matched_entries()   
    
    def matched_entries(self):
        entries = []
        statement_entries = self.ofxreader.entries_by_account()
        sheet_entries = self.sheetreader.entries_by_account()

        for acc_id in statement_entries.keys():
            for stm_entry in statement_entries[acc_id]:
                for sht_entry in sheet_entries[self.matched_acc(acc_id)]:
                    if stm_entry == sht_entry:
                        date = stm_entry.date
                        history = f"{stm_entry.history} - {sht_entry.history}"
                        value = stm_entry.value
                        credit = self.get_account(
                            acc_id) if value < 0 else self.get_account(history)
                        debit = self.get_account(
                            acc_id) if value > 0 else self.get_account(history)
                        entries.append(
                            FullEntry(date=date, history=history, value=value, credit=credit, debit=debit))
                        break
        return entries
    

    def matched_acc(self, val):
        return val

    def get_account(self, history):
        return 259

    def get_bank(self, bank_id):
        return 2
    
