"""
Test harness for the expense tracker API. Run after each fix:
    python3 test_api.py
Uses a throwaway CSV file so it never touches real data.
"""
import os, sys, importlib

TEST_CSV = "TestTracker.csv"
if os.path.exists(TEST_CSV):
    os.remove(TEST_CSV)

# Force tracker/api to use the test CSV
import tracker as tracker_module
orig_init = tracker_module.ExpenseTracker.__init__
def patched_init(self, csv_file=TEST_CSV):
    orig_init(self, csv_file)
tracker_module.ExpenseTracker.__init__ = patched_init

import api as api_module
from fastapi.testclient import TestClient

client = TestClient(api_module.app)

passed = 0
failed = 0

def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}")

print("== add expenses ==")
r1 = client.post("/expenses", json={"category": "Food", "name": "Lunch", "value": "12.50", "date": "2026-09-01T12:00:00"})
check("add expense 1 -> 200", r1.status_code == 200)
r2 = client.post("/expenses", json={"category": "Transport", "name": "Bus", "value": "3.25", "date": "2026-09-01T13:00:00"})
check("add expense 2 -> 200", r2.status_code == 200)
r3 = client.post("/expenses", json={"category": "Food", "name": "Dinner", "value": "20.00", "date": "2026-09-15T19:00:00"})
check("add expense 3 -> 200", r3.status_code == 200)

print("== get all ==")
r = client.get("/expenses")
check("get all -> 200", r.status_code == 200)
check("get all -> 3 items", len(r.json()) == 3)

print("== spending by month (has data) ==")
r = client.get("/expenses/spending/month", params={"month": 9, "year": 2026})
check("Sept 2026 -> 200", r.status_code == 200)
check("Sept 2026 total correct", "35.75" in r.text)

print("== spending by month (no data) -> should 404 ==")
r = client.get("/expenses/spending/month", params={"month": 1, "year": 2020})
check("empty month -> 404", r.status_code == 404)

print("== spending by category (has data) ==")
r = client.get("/expenses/spending/category", params={"category": "Food"})
check("Food category -> 200", r.status_code == 200)
check("Food total correct", "32.50" in r.text)

print("== spending by category (no data) -> should 404 ==")
r = client.get("/expenses/spending/category", params={"category": "Bills"})
check("empty category -> 404", r.status_code == 404)

print("== edit expense ==")
eid = r1.json()["id"]
r = client.patch(f"/expenses/{eid}", json={"value": "15.00"})
check("edit -> 200", r.status_code == 200)
check("edit -> value updated", r.json()["value"] == "15.00")
check("edit -> other fields preserved", r.json()["name"] == "Lunch")

print("== edit nonexistent -> 404 ==")
r = client.patch("/expenses/9999", json={"value": "1.00"})
check("edit missing -> 404", r.status_code == 404)

print("== delete expense ==")
eid3 = r3.json()["id"]
r = client.delete(f"/expenses/{eid3}")
check("delete -> 200", r.status_code == 200)
r = client.get("/expenses")
check("delete -> count now 2", len(r.json()) == 2)

print("== delete nonexistent -> 404 ==")
r = client.delete("/expenses/9999")
check("delete missing -> 404", r.status_code == 404)

print("== search ==")
r = client.get("/expenses/search", params={"name": "bus"})
check("search case-insensitive -> 200", r.status_code == 200)
check("search -> 1 result", len(r.json()) == 1)

print("== filter ==")
r = client.get("/expenses/filter", params={"category": "food"})
check("filter by category (lowercase) -> 200", r.status_code == 200)

print("== categories ==")
r = client.get("/categories")
check("categories -> 200", r.status_code == 200)
check("categories -> contains Food", "Food" in r.json())
check("categories -> exactly 6", len(r.json()) == 6)

print(f"\n{passed} passed, {failed} failed")
if os.path.exists(TEST_CSV):
    os.remove(TEST_CSV)
sys.exit(1 if failed else 0)
