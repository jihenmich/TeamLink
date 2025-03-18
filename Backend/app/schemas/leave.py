from pydantic import BaseModel
from datetime import date

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
    status: str  # Pending, Approved, Rejected

    class Config:
        orm_mode = True
