# app/api/endpoints/leave.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.employee import TimeTrackingCreate, VacationRequestCreate

router = APIRouter()

# Zeiterfassung
@router.post("/time_tracking/")
def add_time_tracking(time_tracking: TimeTrackingCreate, db: Session = Depends(session.get_db)):
    return repository.add_time_tracking(db=db, time_tracking=time_tracking)

@router.get("/time_tracking/{employee_id}")
def get_time_tracking(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_time_tracking_by_employee(db=db, employee_id=employee_id)

# Urlaubsanfragen
@router.post("/vacation_requests/")
def add_vacation_request(vacation_request: VacationRequestCreate, db: Session = Depends(session.get_db)):
    return repository.add_vacation_request(db=db, vacation_request=vacation_request)

@router.get("/vacation_requests/{employee_id}")
def get_vacation_requests(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_vacation_requests_by_employee(db=db, employee_id=employee_id)
