# app/api/endpoints/payroll.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.payroll import PayrollCreate

router = APIRouter()

# Gehaltsabrechnung hinzufügen (ohne employee_id in der URL!)
@router.post("/")
def add_payroll(payroll: PayrollCreate, db: Session = Depends(session.get_db)):
    return repository.add_payroll(db=db, payroll=payroll)

# Gehaltsabrechnungen für einen bestimmten Mitarbeiter abrufen
@router.get("/employee/{employee_id}")
def get_payroll_by_employee(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_payroll_by_employee(db=db, employee_id=employee_id)

# Alle Gehaltsabrechnungen abrufen
@router.get("/")
def get_all_payrolls(db: Session = Depends(session.get_db)):
    return repository.get_all_payrolls(db=db)

# Gehaltsabrechnung löschen
@router.delete("/{payroll_id}")
def delete_payroll(payroll_id: int, db: Session = Depends(session.get_db)):
    return repository.delete_payroll(db=db, payroll_id=payroll_id)
