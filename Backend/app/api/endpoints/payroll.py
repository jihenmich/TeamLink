# app/api/endpoints/payroll.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.payroll import PayrollCreate  # Für Gehaltsabrechnungen
from app.schemas.time_tracking import TimeTrackingCreate  # Falls Zeiterfassung ebenfalls hier benötigt wird
from app.schemas.employee import EmployeeCreate  # Falls Mitarbeiterdaten auch gebraucht werden

router = APIRouter()

# Gehaltsabrechnung hinzufügen
@router.post("/{employee_id}/payroll/")
def add_payroll(employee_id: int, payroll: PayrollCreate, db: Session = Depends(session.get_db)):
    payroll.employee_id = employee_id
    return repository.add_payroll(db=db, payroll=payroll)

# Gehaltsabrechnungen für einen Mitarbeiter abrufen
@router.get("/{employee_id}/payroll/")
def get_payroll(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_payroll_by_employee(db=db, employee_id=employee_id)
