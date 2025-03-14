from sqlalchemy.orm import Session
from app.db.models import Employee
from app.schemas.employee import EmployeeCreate

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def add_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
