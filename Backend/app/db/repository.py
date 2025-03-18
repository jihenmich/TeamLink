# app/db/repository.py
from sqlalchemy.orm import Session
from app.db.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

# Mitarbeiter erstellen
def add_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name, hours_worked=employee.hours_worked)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Alle Mitarbeiter abrufen
def get_employees(db: Session):
    return db.query(Employee).all()

# Mitarbeiter anhand der ID abrufen
def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

# Mitarbeiter aktualisieren
def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db_employee.name = employee.name
        db_employee.hours_worked = employee.hours_worked
        db.commit()
        db.refresh(db_employee)
    return db_employee

# Mitarbeiter löschen
def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
