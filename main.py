#the CLI
from tracker import ExpenseTracker

def menu():
    et = ExpenseTracker()
    while True:
        print("\n====EXPENSE TRACKER====")
        print("\n1. Add expense\n2. Delete expense\n3. Delete all expenses\n4. Search expense\n5. Calculate monthly spending\nq. Exit")
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

            et.add_expense(expense, value)
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

        elif answer == "4":
            expense_name = input("Expense: ")
            result = et.search_expense(expense_name)
            if result is None:
                print("Expense not found")
            else:
                print(f"{result[0]}: {result[1]}$")

        elif answer == "5":
            print(et.calculate_spending())

        elif answer == "q":
            break

        else:
            print("Invalid input. Please try again")

if __name__ == "__main__":
    menu()