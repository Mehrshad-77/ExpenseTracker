#the CLI
import datetime as dt
from tracker import ExpenseTracker

categories = {"F":"Food",
              "T":"Transport",
              "ENT":"Entertainment",
              "EDU":"Education",
              "B":"Bills",
              "O":"Other"
            }

months = {"1" : "January",
          "2" : "February",
          "3" : "March",
          "4" : "April",
          "5" : "May",
          "6" : "June",
          "7" : "July",
          "8" : "August",
          "9" : "September",
          "10" : "October",
          "11" : "November",
          "12" : "December"}

def display_expenses(expenses):
                for expense in expenses:
                    print(
                        f"{expense.id}    "
                        f"{expense.category}    "
                        f"{expense.name}    "
                        f"{expense.value}$    "
                        f"{expense.date.strftime('%Y-%m-%d')}"
                    )

def menu():
    et = ExpenseTracker()
    while True:
        print("\n====EXPENSE TRACKER====")
        print("\n1. Add expense\n2. Delete expense\n3. Search expense\n4. Show all expenses\n5. Calculate spending\n6. Filter expenses\n7. Delete all expenses\nq. Exit")
        answer = input("> ").lower()

        if answer == "1":
            while True:
                try:
                    category = input("Categoty:\nF:Food T:Transport Ent:Entertainment Edu:Education B:Bills O:Other\n> ").upper()
                    if category not in categories:
                        raise ValueError
                    category = categories[category]
                    break
                except ValueError:
                    print("Category doesn't exist")

            expense = input("Expense(Enter for category name): ")
            if expense == "":
                expense = category
            while True:
              try:
                  value = float(input("Value: "))
                  if value <= 0:
                      raise ValueError
                  break
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

            et.add_expense(category, expense, value, date)
            print("Expense was successfully added")

        elif answer == "2":
            while True:
                try:
                    expense_id = int(input("Expense ID: "))
                    if expense_id <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid ID. Please enter a valid ID")
                    continue

            while True:
                check = input("Are you sure you want to delete this expense?(Y/N) ").upper()
                if check == "Y":
                    result = et.delete_expense(expense_id)
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
            results = et.search_expense(expense_name)
            if not results:
                print("Expense not found")
            else:
                for result in results:
                    print(f"ID: {result.id}")
                    print(f"Category: {result.category}")
                    print(f"{result.name}: {result.value}$")
                    print(f"Date: {result.date.strftime('%Y-%m-%d')}")

        elif answer == "4":
            expenses = et.get_expenses()
            if not expenses:
                print("No expenses to show")
            else:
                while True:
                    sort_by = input("Sort by (d:date, v:value, n:name('m' to go back to the menu)): ").lower()
                    if sort_by == "d":
                        sorted_expenses = sorted(expenses, key=lambda expense: expense.date, reverse=True)
                        display_expenses(sorted_expenses)

                    elif sort_by == "v":
                        sorted_expenses = sorted(expenses, key=lambda expense: expense.value, reverse=True)
                        display_expenses(sorted_expenses)

                    elif sort_by == "n":
                        sorted_expenses = sorted(expenses, key=lambda expense: expense.name.lower())
                        display_expenses(sorted_expenses)

                    elif sort_by == "m":
                        break

                    else:
                        print("Invalid input.")

        elif answer == "5":
            while True:
                filter_by = input("By(Category(C)/Month(M))/Menu(B)? ").upper()
                if filter_by == "M":
                    while True:
                        try:
                            month = int(input("Which Month spending you looking for(1-12)? "))
                            if month > 12 or month < 1:
                                raise ValueError
                            else:
                                break
                        except ValueError:
                            print("invalid input. Please enter a legit month")
                            continue
                    while True:
                        year_input = input("Which Year(Enter for current year)? ")

                        if year_input == "":
                            year = dt.datetime.now().year
                            break

                        try:
                            year = int(year_input)

                            if year < 2020 or year > 2100:
                                raise ValueError
                            
                            break

                        except ValueError:
                            print("Invalid input. Please Enter a legit year")
                            continue

                    print(f"{months[str(month)]} {str(year)} total spending: {et.calculate_spending(month, year)}$")
                    break
                elif filter_by == "C":
                    while True:
                        category = input("Categories:\n F: Food\nT: Transport\nENT:Entertainment\nEDU: Education\nB: Bills\nO: Other\nM: Back\n> ").upper()
                        if category == "M":
                            break

                        if category not in categories:
                            print("Invalid category.")
                            continue

                        else:
                            print(f"Money spent on {categories[category]}: {et.calculate_spending_category(categories[category])}$")
                            break
                elif filter_by == "B":
                    break

        elif answer =="6":
            expenses = et.get_expenses()
            filter_by = input("filter by:\n1. Category, 2. Date, m. Menu\n> ").lower()

            if filter_by == "1":
                while True:
                    cat = input("Categories:\n F: Food\nT: Transport\nENT:Entertainment\nEDU: Education\nB: Bills\nO: Other\nM: Back\n> ").upper()

                    if cat == "M":
                        break

                    if cat not in categories:
                        print("Invalid category.")
                        continue

                    filtered = [expense
                                for expense in expenses
                                if expense.category == categories[cat]
                                ]

                    if not filtered:
                        print("No expenses found.\nUse Another category")
                        continue
                    else:
                        display_expenses(filtered)
                        break
            if filter_by == "2":
                while True:
                    date = input("Date(Enter the date(YYYY-MM-DD)): ")
                    try:
                        date = dt.datetime.strptime(date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date. Please use YYYY-MM-DD.")

                filtered = [expense
                            for expense in expenses
                            if expense.date.date() == date.date()
                            ]
                
                if not filtered:
                    print("No expenses found.")
                else:
                    display_expenses(filtered)

        elif answer == "7":
            while True:
                check = input("Are you sure you want to delete all expenses?(Y/N) ").upper()
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
