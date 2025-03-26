from pydantic import BaseModel, validator
from datetime import datetime, date

# Employee Schema für die Erstellung eines Mitarbeiters
class EmployeeCreate(BaseModel):
    name: str  # Beispiel: Der Name des Mitarbeiters
    role: str
    hours_worked: int  # Stunden des Mitarbeiters, z.B. die Anzahl der gearbeiteten Stunden
    
    class Config:
        orm_mode = True  # Damit die Datenbankmodelle korrekt umgewandelt werden

class EmployeeUpdate(BaseModel):
    name: str  # Der Name des Mitarbeiters
    hours_worked: int  # Das Feld für die Stunden des Mitarbeiters

    class Config:
        orm_mode = True  # Damit die Datenbankmodelle korrekt umgewandelt werden


# Zeiterfassung Schema
class TimeTrackingCreate(BaseModel):
    employee_id: int
    clock_in: datetime
    clock_out: datetime
    total_hours: int

    class Config:
        orm_mode = True

# Urlaubsanfragen Schema (nun als Leave)
class LeaveCreate(BaseModel):  # Geändert von VacationRequestCreate zu LeaveCreate
    employee_id: int
    start_date: date
    end_date: date
    status: str = "Pending"  # Standardmäßig 'Pending'

    class Config:
        orm_mode = True


# Urlaubsanfragen Update Schema (nun als Leave)
class LeaveUpdate(BaseModel):  # Geändert von VacationRequestUpdate zu LeaveUpdate
    start_date: date
    end_date: date
    status: str = "Pending"  # Standardmäßig 'Pending'

    @validator('end_date')
    def check_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

    class Config:
        orm_mode = True

# Gehaltsabrechnungen Schema
class PayrollCreate(BaseModel):
    employee_id: int
    salary: float
    payroll_date: date
    deductions: float = 0.0  # Standardwert 0.0 für Abzüge

    class Config:
        orm_mode = True
