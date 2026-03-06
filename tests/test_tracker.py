import pytest
from finance.tracker import FinanceTracker


@pytest.fixture
def tracker():
    t = FinanceTracker()
    t._records = []  # her testte temiz başla, dosyaya dokunma
    return t


def test_add_income(tracker):
    tracker.add(1000, "salary", "income")
    assert tracker.total_income() == 1000


def test_add_expense(tracker):
    tracker.add(200, "food", "expense")
    assert tracker.total_expense() == 200


def test_balance(tracker):
    tracker.add(1000, "salary", "income")
    tracker.add(300, "rent", "expense")
    assert tracker.balance() == 700


def test_by_category(tracker):
    tracker.add(500, "food", "expense")
    tracker.add(300, "food", "expense")
    tracker.add(200, "transport", "expense")
    result = tracker.by_category("expense")
    assert result["food"] == 800
    assert result["transport"] == 200


def test_by_month(tracker):
    from datetime import date
    tracker.add(1000, "salary", "income", record_date=date(2026, 1, 1))
    tracker.add(500,  "rent",   "expense", record_date=date(2026, 1, 15))
    result = tracker.by_month()
    assert result["2026-01"]["income"] == 1000
    assert result["2026-01"]["expense"] == 500