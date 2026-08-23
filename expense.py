import os
import csv
import datetime

#a class for expenses
class Expense:
    def __init__(self, name, value, date):
        self.name = name
        self.value = value
        self.date = date

class ExpenseTracker:
    def __init__(self, csv_file = "Tracker.csv"):
        self.expenses = []
        self.load_from_csv()

    def save_to_csv(self):
        with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["Expense", "Value"])

            for expense in self.expenses:
                writer.writerow([
                    expense.name,
                    expense.value
                ])

    def load_from_csv(self):
        if not os.path.exists(self.csv_file):
            return

        with open(self.csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader, None) #skips Header

            self.tasks = [Expense(*row) for row in reader]

    def add_expense(self, expense, value):
        expense = Expense(expense,
                          value)
        self.expenses.append(expense)
        self.save_to_csv()
        print("Expense added")

    def delete_expense(self, expense_name):
         for expense in self.expenses:
            if expense.name.lower() == expense_name:
                self.expenses.remove(expense)
                self.save_to_csv()
                print("expense removed succesfully")
            else:
                print("Expense does not exist")

    def delete_all_expenses(self):
        self.expenses.clear()
        self.save_to_csv()
        print("All expenses removed")

    def search_expense(self, expense_name):
        for expense in self.expenses:
            if self.expense.name.lower() == expense_name:
                print(f"Expense: {expense.name}, Value: {expense.value}")
            else:
                print("Expense does not exist")

    def calculate_spending(self):
        expenses_sum = 0
        for expense in self.expenses:
            expenses_sum += expense.value
        print(f"This Months Expenses: {expense.value}")
        self.save_to_csv()