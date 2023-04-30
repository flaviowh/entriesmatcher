from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class AccountsInfo(ABC):
    def __init__(self, company_id) -> None:
        self.company_id = company_id

    @abstractmethod
    def get_credit_account_and_history(self, keywords: str) -> Tuple[int, str]:
        pass

    @abstractmethod
    def get_debit_account_and_history(self, keywords: str) -> Tuple[int, str]:
        pass

    @abstractmethod
    def set_credit_account(self, keywords: List[str], acc_id: int, history: str) -> None:
        pass

    @abstractmethod
    def set_debit_account(self, keywords: List[str], acc_id: int, history: str) -> None:
        pass

    @abstractmethod
    def get_bank_account(self, bank_id: str) -> int:
        pass


class FakeAccountDB(AccountsInfo):
    def __init__(self) -> None:
        self.data = {"credits": {"default": {"acc_id" : "2", "history": "received"}},
                      "debits": {
                "default": {"acc_id" : "259", "history": "paid"}}, 
                "banks": {"default": "56"}}

    def get_credit_account_and_history(self, keywords: str) -> Tuple[int, str]:
        info = self.data["credits"]["default"]
        return info["acc_id"], info.get("history", "")

    def get_debit_account_and_history(self, keywords: str) -> Tuple[int, str]:
        info = self.data["debits"]["default"]
        return info["acc_id"], info.get("history", "")

    def set_credit_account(self, keywords: List[str], acc_id: int, history: str) -> None:
        self.data["credits"][" ".join(keywords)] = {"acc_id" : acc_id, "history": history}

    def set_debit_account(self, keywords: List[str], acc_id: int, history: str) -> None:
        self.data["debits"][" ".join(keywords)] = {"acc_id" : acc_id, "history": history}

    def get_bank_account(self, bank_id: str) -> int:
        return int(self.data["banks"][bank_id])
