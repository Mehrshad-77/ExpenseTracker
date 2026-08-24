#the CLI
import datetime as dt
from tracker import ExpenseTracker

def menu():
    et = ExpenseTracker()
    while True:
        print("\n====EXPENSE TRACKER====")
        print("\n1. Add expense\n2. Delete expense\n3. Search expense\n4. Show all expenses\n5. Calculate monthly spending\n6. Delete all expenses\nq. Exit")
        answer = input("> ").lower()

        if answer == "1":
            expense = input("Expense: ")
            try:
                value = float(input("Value: "))
                if value <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid input. please enter a valid number for value.")
                continue
            
            while True:
                date_input = input("Date(Enter the date(YYYY-MM-DD), Enter for today): ")
                if date_input == "":
                    date = dt.datetime.now()
                    break
                try:
                    date = dt.datetime.strptime(date_input, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date. Please use YYYY-MM-DD.")

            et.add_expense(expense, value, date)
            print("Expense was successfully added")

        elif answer == "2":
            expense_name = input("Expense: ")
            while True:
                check = input("Are you sure you want to delete this expense? ").upper()
                if check == "Y":
                    result = et.delete_expense(expense_name)
                    if result:
                        print("Expense successfully deleted.")
                    else:
                        print("Expense not found")
                    break
                elif check == "N":
                    break
                else:
                    print("Invalid input. Please try again")

        elif answer == "3":
            expense_name = input("Expense: ")
            result = et.search_expense(expense_name)
            if result is None:
                print("Expense not found")
            else:
                print(f"{result.name}: {result.value}$")
                print(f"Date: {result.date.strftime('%Y-%m-%d')}")

        elif answer == "4":
            expenses = et.get_expenses()
            if not expenses:
                print("No expenses to show")
            else:
                sorted_expenses = sorted(expenses, key=lambda expense: expense.date, reverse=True)
                for i, expense in enumerate(sorted_expenses, start=1):
                    print(f"{i}. {expense.name}    "
                          f"{expense.value}    "
                          f"{expense.date.strftime('%Y-%m-%d')}"
                          )
            while True:
                sort_by = input("Sort by (d:date, v:value, n:name('m' to go back to the menu)): ").lower()
                if sort_by == "d":
                    sorted_expenses = sorted(expenses, key=lambda expense: expense.date, reverse=True)
                    for i, expense in enumerate(sorted_expenses, start=1):
                        print(f"{i}. {expense.name}    "
                            f"{expense.value}    "
                            f"{expense.date.strftime('%Y-%m-%d')}"
                            )
                elif sort_by == "v":
                    sorted_expenses = sorted(expenses, key=lambda expense: expense.value, reverse=True)
                    for i, expense in enumerate(sorted_expenses, start=1):
                        print(f"{i}. {expense.name}    "
                              f"{expense.value}    "
                              f"{expense.date.strftime('%Y-%m-%d')}"
                              )
                elif sort_by == "n":
                    sorted_expenses = sorted(expenses, key=lambda expense: expense.name, reverse=False)
                    for i, expense in enumerate(sorted_expenses, start=1):
                        print(f"{i}. {expense.name}    "
                              f"{expense.value}    "
                              f"{expense.date.strftime('%Y-%m-%d')}"
                              )
                elif sort_by == "m":
                    break
                else:
                    print("Invalid input.")


        elif answer == "5":
            print(et.calculate_spending())

        elif answer == "6":
            while True:
                check = input("Are you sure you want to delete all expenses? ").upper()
                if check == "Y":
                    et.delete_all_expenses()
                    print("Expenses were deleted successfully")
                    break
                elif check == "N":
                    break
                else:
                    print("Invalid input. Please try again")

        elif answer == "q":
            break

        else:
            print("Invalid input. Please try again")

if __name__ == "__main__":
    menu()