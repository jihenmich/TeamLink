from pydantic import BaseModel
from datetime import date

# Gehaltsabrechnung Schema
class PayrollCreate(BaseModel):
    employee_id: int
    salary: float
    payroll_date: date
    deductions: float = 0.0  # Standardwert 0.0 für Abzüge

    class Config:
        orm_mode = True

# Gehaltsabrechnung Update Schema
class PayrollUpdate(BaseModel):
    salary: float
    payroll_date: date
    deductions: float = 0.0

    class Config:
        orm_mode = True
