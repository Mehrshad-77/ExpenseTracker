import os
import csv
import datetime

#a class for expenses
class Expense:
    def __init__(self, name, value, date):
        self.name = name
        self.value = float(value)

        if isinstance(date, str):
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            self.date = date

class ExpenseTracker:
    def __init__(self, csv_file = "Tracker.csv"):
        self.csv_file = csv_file
        self.expenses = []
        self.load_from_csv()

    def save_to_csv(self):
        with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["Expense", "Value", "Date"])

            for expense in self.expenses:
                writer.writerow([
                    expense.name,
                   expense.value,
                    expense.date.strftime("%Y-%m-%d")
                ])

    def load_from_csv(self):
        if not os.path.exists(self.csv_file):
            return

        with open(self.csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader, None) #skips Header

            for row in reader:
                name, value, date = row
                self.expenses.append(Expense(name, value, date))

    def add_expense(self, expense, value, date=None):
        if date is None:
            date = datetime.datetime.now()

        expense = Expense(expense, value, date)
        self.expenses.append(expense)
        self.save_to_csv()

    def delete_expense(self, expense_name):
        for expense in self.expenses:
            if expense.name.lower() == expense_name.lower():
                self.expenses.remove(expense)
                self.save_to_csv()
                return True
            
        return False

    def delete_all_expenses(self):
        self.expenses.clear()
        self.save_to_csv()

    def search_expense(self, expense_name):
        for expense in self.expenses:
            if expense.name.lower() == expense_name.lower():
                return expense

    def calculate_spending(self):
        expenses_sum = 0
        today = datetime.datetime.now()
        for expense in self.expenses:
            if expense.date.year == today.year and expense.date.month == today.month:
                expenses_sum += expense.value
        return expenses_sum