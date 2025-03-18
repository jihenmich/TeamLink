# app/api/endpoints/payroll.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.employee import PayrollCreate

router = APIRouter()

@router.post("/payroll/")
def add_payroll(payroll: PayrollCreate, db: Session = Depends(session.get_db)):
    return repository.add_payroll(db=db, payroll=payroll)

@router.get("/payroll/{employee_id}")
def get_payroll(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_payroll_by_employee(db=db, employee_id=employee_id)
