import os
import csv
import datetime
from decimal import Decimal

#a class for expenses
class Expense:
    def __init__(self,id, category, name, value, date):
        self.id = int(id)
        self.category = category
        self.name = name
        self.value = Decimal(str(value))

        if isinstance(date, str):
            try:
                self.date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            self.date = date

class ExpenseTracker:
    def __init__(self, csv_file = "Tracker.csv"):
        self.csv_file = csv_file
        self.expenses = []
        self.load_from_csv()

    def save_to_csv(self):
        try:
            with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Category", "Name", "Value", "Date"])
                for expense in self.expenses:
                    writer.writerow([
                        expense.id,
                        expense.category,
                        expense.name,
                        expense.value,
                        expense.date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    ])
        except OSError as e:
            print(f"Could not save expenses to {self.csv_file}: {e}")

    def load_from_csv(self):
        if not os.path.exists(self.csv_file):
            return

        try:
            with open(self.csv_file, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)  # skips Header
                for row in reader:
                    try:
                        id, category, name, value, date = row
                        self.expenses.append(Expense(id, category, name, value, date))
                    except ValueError:
                        print("Rows don't match")
                        continue
        except (OSError, UnicodeDecodeError) as e:
            print(f"Could not read expenses from {self.csv_file}: {e}")

    def add_expense(self, category, name, value, date=None):
        if date is None:
            date = datetime.datetime.now()

        id = max((expense.id for expense in self.expenses), default=0)
        id +=1

        expense = Expense(id, category, name, value, date)
        self.expenses.append(expense)
        self.save_to_csv()

    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense.id == expense_id:
                self.expenses.remove(expense)
                self.save_to_csv()
                return True
            
        return False

    def delete_all_expenses(self):
        self.expenses.clear()
        self.save_to_csv()

    def search_expense(self, expense_name):
        return [expense for expense in self.expenses if expense.name.lower().strip() == expense_name.lower().strip()]

    def calculate_spending(self, month, year):
        expenses_sum = Decimal("0")
        for expense in self.expenses:
            if expense.date.month == month and expense.date.year == year:
                expenses_sum += expense.value
        return expenses_sum

    def get_expenses(self):
        return self.expenses.copy()

    def calculate_spending_category(self, category):
        expenses_sum = Decimal("0")
        for expense in self.expenses:
            if expense.category.lower().strip() == category.lower().strip():
                expenses_sum += expense.value
        return expenses_sum