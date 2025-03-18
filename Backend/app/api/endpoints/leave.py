# app/api/endpoints/leave.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.leave import LeaveCreate, LeaveUpdate  # Geändert von VacationRequestCreate zu LeaveCreate
from app.schemas.time_tracking import TimeTrackingCreate  # Falls Zeiterfassung ebenfalls hier verwendet werden muss
from app.schemas.payroll import PayrollCreate  # Falls Gehaltsabrechnungen auch benötigt werden

router = APIRouter()

# Zeiterfassung hinzufügen
@router.post("/time_tracking/")  # Der Pfad zum Hinzufügen einer Zeiterfassung
def add_time_tracking(time_tracking: TimeTrackingCreate, db: Session = Depends(session.get_db)):
    return repository.add_time_tracking(db=db, time_tracking=time_tracking)

# Zeiterfassungen für einen Mitarbeiter abrufen
@router.get("/time_tracking/{employee_id}")  # Hier nach Mitarbeiter-ID suchen
def get_time_tracking(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_time_tracking_by_employee(db=db, employee_id=employee_id)

# Urlaubsanfrage (Leave) hinzufügen
@router.post("/{employee_id}/leave/")  # Geändert von /vacation-request/ zu /leave/
def add_leave(employee_id: int, leave_request: LeaveCreate, db: Session = Depends(session.get_db)):
    leave_request.employee_id = employee_id
    return repository.add_leave(db=db, leave_request=leave_request)

# Urlaubsanfragen (Leaves) für einen Mitarbeiter abrufen
@router.get("/{employee_id}/leave/")  # Hier nach Mitarbeiter-ID suchen
def get_leaves(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_leaves_by_employee(db=db, employee_id=employee_id)

# Urlaubsanfrage aktualisieren
@router.put("/leave/{leave_id}")  # Geändert von /vacation_requests/ zu /leave/
def update_leave(leave_id: int, leave_request: LeaveUpdate, db: Session = Depends(session.get_db)):
    return repository.update_leave(db=db, leave_id=leave_id, leave_request=leave_request)

# Urlaubsanfrage löschen
@router.delete("/leave/{leave_id}")  # Geändert von /vacation_requests/ zu /leave/
def delete_leave(leave_id: int, db: Session = Depends(session.get_db)):
    return repository.delete_leave(db=db, leave_id=leave_id)
