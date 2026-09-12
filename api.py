from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from decimal import Decimal
from tracker import ExpenseTracker
from typing import Literal, Optional
import datetime
import os

CATEGORIES = ["Food", "Transport", "Entertainment", "Education", "Bills", "Other"]


class ExpenseOut(BaseModel):
    id: int
    category: str
    name: str
    value: Decimal
    date: datetime.datetime

class Expensein(BaseModel):
    category: Literal[*CATEGORIES]
    name: str
    value: Decimal = Field(gt=0)
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)

class ExpenseUpdate(BaseModel):
    category: Optional[Literal[*CATEGORIES]] = None
    name: Optional[str] = None
    value: Optional[Decimal] = Field(default=None, gt=0)
    date: Optional[datetime.datetime] = None


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


app = FastAPI()

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "expense-tracker-preview.html")

et = ExpenseTracker()


@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND_PATH)

@app.get("/categories", response_model=list[str])
def get_categories():
    return CATEGORIES

@app.get("/expenses", response_model=list[ExpenseOut])
def get_expenses():
    return et.get_expenses()

@app.post("/expenses", response_model=ExpenseOut)
def add_expense(expense: Expensein):
    return et.add_expense(expense.category, expense.name, expense.value, expense.date)

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    result = et.delete_expense(expense_id)
    if result:
        return {"message": "Expense deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Expense not found.")

@app.patch("/expenses/{expense_id}", response_model=ExpenseOut)
def edit_expense(expense_id: int, expense: ExpenseUpdate):
    result = et.edit_expense(
        expense_id,
        category=expense.category,
        name=expense.name,
        value=expense.value,
        date=expense.date,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found.")
    return result

@app.get("/expenses/search", response_model=list[ExpenseOut])
def search_expense(name: str):
    result = et.search_expense(name)
    if not result:
        raise HTTPException(status_code=404, detail="Expense not found.")
    return result

@app.get("/expenses/spending/month")
def calculate_spending(month: int, year: int):
    spending = et.calculate_spending(month, year)
    if spending is None:
        raise HTTPException(status_code=404, detail="No expenses found for the specified month and year.")
    return f"{months[str(month)]} {year} Total spending: ${spending:.2f}"

@app.get("/expenses/spending/category")
def calculate_spending_category(category: str):
    total_spending = et.calculate_spending_category(category)
    if total_spending is None:
        raise HTTPException(status_code=404, detail="No expenses found for the specified category.")
    return f"{category} Total spending: ${total_spending:.2f}"

@app.get("/expenses/filter", response_model=list[ExpenseOut])
def filter_expenses(category: Optional[str] = None, month: Optional[int] = None):
    filtered_expenses = et.get_expenses()

    if category:
        filtered_expenses = [expense for expense in filtered_expenses if expense.category.lower().strip() == category.lower().strip()]
        if not filtered_expenses:
            raise HTTPException(status_code=404, detail="No expenses found for the specified category.")
    
    if month:
        filtered_expenses = [expense for expense in filtered_expenses if expense.date.month == month]
        if not filtered_expenses:
            raise HTTPException(status_code=404, detail="No expenses found for the specified month.")

    return filtered_expenses

@app.delete("/expenses")
def delete_all_expenses():
    delete_all = et.delete_all_expenses()
    if delete_all:
        return {"message": "All expenses deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="No expense found.")