from dataclasses import dataclass
from abc import ABC, abstractmethod
from decimal import Decimal
import pandas as pd
pd.options.display.max_rows = 1000
pd.options.display.max_rows = 1000

# DATA CLASSES


@dataclass
class Entry:
    date: str
    history: str
    value: Decimal

    def __eq__(self, other):
        if isinstance(other, Entry):
            return self.date == other.date and self.value == other.value
        return False


@dataclass
class SheetEntry(Entry):
    description: str
    bank_id: str

    def __eq__(self, other):
        return super().__eq__(other)


@dataclass
class StatementEntry(Entry):
    bank_id: str

    def __eq__(self, other):
        return super().__eq__(other)


@dataclass
class FullEntry(Entry):
    credit: int
    debit: int


# READER CLASS

class EntriesReader(ABC):
    @abstractmethod
    def all_entries(self):
        pass
    
    def entries_by_account(self):
        entries = {}
        for entry in self.all_entries():
            if entry.bank_id != None:
                entries[entry.bank_id] = entries.get(entry.bank_id, []) + [entry]
            else:
                entries["unknown"] = entries.get("unknown", []) + [entry]

        return entries

    def total_transactions(self):
        total = 0
        for entry in self.all_entries():
            total += entry.value
        return total

    def to_dataframe(self):
        data = []
        for entry in self.all_entries():
            data.append(vars(entry))
        return pd.DataFrame(data)





