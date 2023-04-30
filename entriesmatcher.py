
from typing import Dict, List, Tuple
from .db_interface import AccountsInfo
from .readers.sheetreader import SheetReader
from .readers.base import EntriesReader, EntryType, FullEntry, SheetEntry


class EntriesMatcher(EntriesReader):
    def __init__(self, statement_reader: EntriesReader, sheet_reader: SheetReader, accounts_keeper: AccountsInfo):
        self.statement_reader = statement_reader
        self.sheet_reader = sheet_reader
        self.accounts_keeper = accounts_keeper
        self.match_count = 0

    def all_entries(self):
        return self.match_entries()

    def match_entries(self) -> List[FullEntry]:
        entries = []

        statement_entries = self.statement_reader.entries_by_account()
        self.sheet_entries = self.sheet_reader.entries_by_account()

        for acc_id in statement_entries.keys():
            for stm_entry in statement_entries[acc_id]:
                value = stm_entry.value
                date = stm_entry.date
                history = stm_entry.history

                for sht_entry in self.sheet_entries[acc_id]:
                    if stm_entry == sht_entry and not sht_entry.matched:
                        history = f"{history} - {sht_entry.history} {sht_entry.description}"
                        self.match_count += 1
                        sht_entry.matched = True
                        break
                if value > 0:
                    debit = self.accounts_keeper.get_bank_account(acc_id)    
                    credit, db_hist = self.accounts_keeper.get_credit_account_and_history(history)
                else:
                    debit, db_hist = self.accounts_keeper.get_debit_account_and_history(history)   
                    credit = self.accounts_keeper.get_bank_account(acc_id)   

                history = f"{db_hist} {history}".strip()
                entries.append(
                    FullEntry(date=date, history=history, value=value, credit=credit, debit=debit))

        return entries

    @property
    def unmatched_entries(self) -> List[SheetEntry]:
        unmatched : List[SheetEntry] = []
        if not self.sheet_entries:
            return unmatched

        for entries in self.sheet_entries.values():
            for e in entries:
                if not e.matched:
                    unmatched.append(e)
        return unmatched
