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
                value = input("Value: ")
                et.add_expense(expense, value)
                print("Succesfully added")
                if value != float(value):
                    raise ValueError
                
            except ValueError:
                print("Invalid input. please enter a number for value.")

        elif answer == "2":
            expense_name = input("Expense: ")
            check = input("Are you sure you want to delete this expense? ").upper()
            if check == "Y":
                result = et.delete_expense(expense_name)
                if result == None:
                    print("Expense not found")
                else:
                    print(result)
            elif check == "N":
                pass
            else:
                print("Invalid input. Please try again")

        elif answer == "3":
            check = input("Are you sure you want to delete all expenses? ").upper()
            if check == "Y":
                et.delete_all_expenses()
            elif check == "N":
                pass
            else:
                print("Invalid input. Please try again")

        elif answer == "4":
            expense_name = input("Expense: ")
            result = et.search_expense(expense_name)
            if result == None:
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