import datetime
from decimal import Decimal

import pytest

from tracker import ExpenseTracker


@pytest.fixture
def tracker(tmp_path):
    csv_file = tmp_path / "test_tracker.csv"
    return ExpenseTracker(csv_file=str(csv_file))


# --- add_expense / auto-incrementing ID ---

def test_add_expense_assigns_sequential_ids(tracker):
    tracker.add_expense("Food", "Lunch", "10.00")
    tracker.add_expense("Food", "Dinner", "15.00")
    ids = [expense.id for expense in tracker.get_expenses()]
    assert ids == [1, 2]


def test_add_expense_ids_continue_after_reload(tracker):
    tracker.add_expense("Food", "Lunch", "10.00")
    reloaded = ExpenseTracker(csv_file=tracker.csv_file)
    reloaded.add_expense("Food", "Dinner", "15.00")
    ids = [expense.id for expense in reloaded.get_expenses()]
    assert ids == [1, 2]


# --- delete_expense ---

def test_delete_expense_found(tracker):
    tracker.add_expense("Food", "Lunch", "10.00")
    assert tracker.delete_expense(1) is True
    assert tracker.get_expenses() == []


def test_delete_expense_not_found(tracker):
    tracker.add_expense("Food", "Lunch", "10.00")
    assert tracker.delete_expense(999) is False
    assert len(tracker.get_expenses()) == 1


# --- search_expense ---

def test_search_expense_returns_all_matches_case_and_whitespace_insensitive(tracker):
    tracker.add_expense("Food", "Coffee", "3.50")
    tracker.add_expense("Food", "coffee ", "4.00")
    results = tracker.search_expense(" COFFEE")
    assert len(results) == 2


def test_search_expense_no_match_returns_empty_list(tracker):
    tracker.add_expense("Food", "Coffee", "3.50")
    assert tracker.search_expense("Tea") == []


# --- edit_expense ---

def test_edit_expense_updates_only_given_fields(tracker):
    tracker.add_expense("Food", "Coffee", "3.50")
    original_date = tracker.get_expenses()[0].date
    tracker.edit_expense(1, value="5.00")
    expense = tracker.get_expenses()[0]
    assert expense.category == "Food"
    assert expense.name == "Coffee"
    assert expense.value == Decimal("5.00")
    assert expense.date == original_date


def test_edit_expense_not_found(tracker):
    assert tracker.edit_expense(999, name="X") is False


def test_edit_expense_keeps_id_stable(tracker):
    tracker.add_expense("Food", "Coffee", "3.50")
    tracker.edit_expense(1, category="Bills")
    assert tracker.get_expenses()[0].id == 1


# --- calculate_spending / calculate_spending_category ---

def test_calculate_spending_filters_by_month_and_year(tracker):
    tracker.add_expense("Food", "Jan expense", "10.00", date=datetime.datetime(2026, 1, 15))
    tracker.add_expense("Food", "Feb expense", "20.00", date=datetime.datetime(2026, 2, 15))
    assert tracker.calculate_spending(1, 2026) == Decimal("10.00")


def test_calculate_spending_category_case_and_whitespace_insensitive(tracker):
    tracker.add_expense("Food", "Lunch", "10.00")
    tracker.add_expense("Bills", "Rent", "500.00")
    assert tracker.calculate_spending_category(" food ") == Decimal("10.00")


# --- Decimal precision (regression test for the float -> Decimal fix) ---

def test_decimal_precision_avoids_float_drift(tracker):
    for _ in range(10):
        tracker.add_expense("Other", "Small charge", "0.10")
    total = sum((expense.value for expense in tracker.get_expenses()), Decimal("0"))
    assert total == Decimal("1.00")


# --- CSV round-trip ---

def test_csv_round_trip_preserves_exact_value_and_fields(tracker):
    tracker.add_expense("Food", "Lunch", "12.50")
    reloaded = ExpenseTracker(csv_file=tracker.csv_file)
    expense = reloaded.get_expenses()[0]
    assert expense.id == 1
    assert expense.category == "Food"
    assert expense.name == "Lunch"
    assert expense.value == Decimal("12.50")


def test_load_from_csv_skips_malformed_row(tmp_path, capsys):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text(
        "ID,Category,Name,Value,Date\n"
        "1,Food,Lunch,10.00,2026-01-01 12:00:00.000000\n"
        "not,enough,fields\n"
        "2,Food,Dinner,15.00,2026-01-01 18:00:00.000000\n"
    )
    tracker = ExpenseTracker(csv_file=str(csv_file))
    captured = capsys.readouterr()
    assert "Rows don't match" in captured.out
    ids = [expense.id for expense in tracker.get_expenses()]
    assert ids == [1, 2]


# --- get_expenses returns a copy ---

def test_get_expenses_returns_a_copy(tracker):
    tracker.add_expense("Food", "Lunch", "10.00")
    expenses = tracker.get_expenses()
    expenses.clear()
    assert len(tracker.get_expenses()) == 1


# --- I/O safety (regression tests for the OSError-handling fix) ---

def test_save_to_csv_handles_os_error_without_crashing(tracker, monkeypatch, capsys):
    tracker.add_expense("Food", "Lunch", "10.00")

    def raise_os_error(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr("builtins.open", raise_os_error)
    tracker.save_to_csv()  # must not raise
    captured = capsys.readouterr()
    assert "Could not save expenses" in captured.out


def test_load_from_csv_handles_os_error_without_crashing(tmp_path, monkeypatch, capsys):
    csv_file = tmp_path / "test_tracker.csv"
    csv_file.write_text("ID,Category,Name,Value,Date\n1,Food,Lunch,10.00,2026-01-01 12:00:00.000000\n")

    def raise_os_error(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr("builtins.open", raise_os_error)
    tracker = ExpenseTracker(csv_file=str(csv_file))  # must not raise
    captured = capsys.readouterr()
    assert "Could not read expenses" in captured.out
    assert tracker.get_expenses() == []
