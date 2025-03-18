from pydantic import BaseModel
from datetime import datetime

# Zeiterfassung Schema
class TimeTrackingCreate(BaseModel):
    employee_id: int
    clock_in: datetime
    clock_out: datetime
    total_hours: int

    class Config:
        orm_mode = True

# Zeiterfassung Update Schema
class TimeTrackingUpdate(BaseModel):
    clock_in: datetime
    clock_out: datetime
    total_hours: int

    class Config:
        orm_mode = True
