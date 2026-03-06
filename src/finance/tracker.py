from datetime import date
from collections import defaultdict
from typing import Optional
import json
import os

DATA_FILE = os.path.expanduser("~/.finance_data.json")


class FinanceTracker:

    def __init__(self):
        self._records: list[dict] = []
        self._load()

    def _load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self._records = json.load(f)

    def _save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self._records, f, indent=2)

    def add(
        self,
        amount: float,
        category: str,
        type: str,
        description: str = "",
        record_date: Optional[date] = None,
    ) -> dict:
        record = {
            "amount":      round(amount, 2),
            "category":    category,
            "type":        type,
            "description": description,
            "date":        (record_date or date.today()).isoformat(),
        }
        self._records.append(record)
        self._save()
        return record

    def total_income(self) -> float:
        return sum(r["amount"] for r in self._records if r["type"] == "income")

    def total_expense(self) -> float:
        return sum(r["amount"] for r in self._records if r["type"] == "expense")

    def balance(self) -> float:
        return round(self.total_income() - self.total_expense(), 2)

    def by_category(self, type: Optional[str] = None) -> dict[str, float]:
        result = defaultdict(float)
        records = self._records
        if type:
            records = [r for r in records if r["type"] == type]
        for r in records:
            result[r["category"]] += r["amount"]
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def by_month(self) -> dict[str, dict]:
        result = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        for r in self._records:
            month = r["date"][:7]
            result[month][r["type"]] += r["amount"]
        return dict(sorted(result.items()))

    def all(self) -> list[dict]:
        return sorted(self._records, key=lambda x: x["date"], reverse=True)