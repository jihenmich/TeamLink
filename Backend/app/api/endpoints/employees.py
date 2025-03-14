from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repository import get_employee_by_id, add_employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter()

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return get_employee_by_id(db, employee_id)

@router.post("/employees/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return add_employee(db, employee)
