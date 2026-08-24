#the CLI
from expense import ExpenseTracker

def menu():
    et = ExpenseTracker()
    while True:
        print("\n====EXPENSE TRACKER====")
        print("\n1. Add expense\n2. Delete expense\n3. Delete all expenses\n4. Search expense\n5. Calculate monthly spending\nq. Exit")
        answer = input("> ").lower()

        if answer == "1":
            expense = input("Expense: ")
            value = input("Value: ")
            et.add_expense(expense, value)
            print("Succesfully added")

        elif answer == "2":
            expense_name = input("Expense: ")
            check = input("Are you sure you want to delete this expense? ").upper()
            if check == "Y":
                et.delete_expense(expense_name)
            elif check == "N":
                continue
            else:
                print("Invalid input. Please try again")

        elif answer == "3":
            check = input("Are you sure you want to delete this expense? ").upper()
            if check == "Y":
                et.delete_all_expenses()
            elif check == "N":
                continue
            else:
                print("Invalid input. Please try again")

        elif answer == "4":
            expense_name = input("Expense: ")
            print(f"{et.search_expense(expense_name)[0]}: {et.search_expense(expense_name)[1]}$")

        elif answer == "5":
            print(et.calculate_spending())

        elif answer == "q":
            break

        else:
            print("Invalid input. Please try again")

if __name__ == "__main__":
    menu()