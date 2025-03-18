# app/api/endpoints/employees.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.schemas.time_tracking import TimeTrackingCreate
from app.schemas.leave import LeaveCreate  # Geändert von VacationRequestCreate zu LeaveCreate
from app.schemas.payroll import PayrollCreate

router = APIRouter()

# Mitarbeiter erstellen
@router.post("/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(session.get_db)):
    return repository.add_employee(db=db, employee=employee)

# Alle Mitarbeiter abrufen
@router.get("/")
def get_employees(db: Session = Depends(session.get_db)):
    return repository.get_employees(db=db)

# Mitarbeiter anhand der ID abrufen
@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_employee_by_id(db=db, employee_id=employee_id)

# Mitarbeiter aktualisieren
@router.put("/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(session.get_db)):
    return repository.update_employee(db=db, employee_id=employee_id, employee=employee)

# Mitarbeiter löschen
@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.delete_employee(db=db, employee_id=employee_id)

# Zeiterfassung hinzufügen
@router.post("/{employee_id}/time-tracking/")
def add_time_tracking(employee_id: int, time_tracking: TimeTrackingCreate, db: Session = Depends(session.get_db)):
    time_tracking.employee_id = employee_id
    return repository.add_time_tracking(db=db, time_tracking=time_tracking)

# Urlaubsanfrage (Leave) hinzufügen
@router.post("/{employee_id}/leave/")  # Geändert von /vacation-request/ zu /leave/
def add_leave(employee_id: int, leave_request: LeaveCreate, db: Session = Depends(session.get_db)):
    leave_request.employee_id = employee_id
    return repository.add_leave(db=db, leave_request=leave_request)

# Gehaltsabrechnung hinzufügen
@router.post("/{employee_id}/payroll/")
def add_payroll(employee_id: int, payroll: PayrollCreate, db: Session = Depends(session.get_db)):
    payroll.employee_id = employee_id
    return repository.add_payroll(db=db, payroll=payroll)
