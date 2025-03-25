from sqlalchemy.orm import Session
from app.db.models import Employee, TimeTracking, Leave, Payroll, User
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.schemas.time_tracking import TimeTrackingCreate, TimeTrackingUpdate
from app.schemas.leave import LeaveCreate, LeaveUpdate
from app.schemas.payroll import PayrollCreate, PayrollUpdate

# --- Mitarbeiterfunktionen ---
def add_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name, hours_worked=employee.hours_worked)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(db: Session):
    return db.query(Employee).all()

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db_employee.name = employee.name
        db_employee.hours_worked = employee.hours_worked
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee

# --- Zeiterfassungsfunktionen ---
def add_time_tracking(db: Session, time_tracking: TimeTrackingCreate):
    db_time_tracking = TimeTracking(
        employee_id=time_tracking.employee_id,
        clock_in=time_tracking.clock_in,
        clock_out=time_tracking.clock_out,
        total_hours=time_tracking.total_hours
    )
    db.add(db_time_tracking)
    db.commit()
    db.refresh(db_time_tracking)
    return db_time_tracking

def get_time_tracking_by_employee(db: Session, employee_id: int):
    return db.query(TimeTracking).filter(TimeTracking.employee_id == employee_id).all()

def update_time_tracking(db: Session, time_tracking_id: int, time_tracking: TimeTrackingUpdate):
    db_time_tracking = db.query(TimeTracking).filter(TimeTracking.id == time_tracking_id).first()
    if db_time_tracking:
        db_time_tracking.clock_in = time_tracking.clock_in
        db_time_tracking.clock_out = time_tracking.clock_out
        db_time_tracking.total_hours = time_tracking.total_hours
        db.commit()
        db.refresh(db_time_tracking)
        return db_time_tracking
    return None

def delete_time_tracking(db: Session, time_tracking_id: int):
    db_time_tracking = db.query(TimeTracking).filter(TimeTracking.id == time_tracking_id).first()
    if db_time_tracking:
        db.delete(db_time_tracking)
        db.commit()
    return db_time_tracking

# ➕ NEU: Alle Zeiterfassungen abrufen
def get_all_time_tracking(db: Session):
    return db.query(TimeTracking).all()

# --- Urlaubsanfragen (Leave) Funktionen ---
def add_leave(db: Session, leave_request: LeaveCreate):
    db_leave_request = Leave(
        employee_id=leave_request.employee_id,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        status=leave_request.status
    )
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

def get_leaves_by_employee(db: Session, employee_id: int):
    return db.query(Leave).filter(Leave.employee_id == employee_id).all()

def update_leave(db: Session, leave_id: int, leave_request: LeaveUpdate):
    db_leave_request = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave_request:
        db_leave_request.start_date = leave_request.start_date
        db_leave_request.end_date = leave_request.end_date
        db_leave_request.status = leave_request.status
        db.commit()
        db.refresh(db_leave_request)
    return db_leave_request

def delete_leave(db: Session, leave_id: int):
    db_leave_request = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave_request:
        db.delete(db_leave_request)
        db.commit()
    return db_leave_request

# ➕ NEU: Alle Urlaubsanfragen abrufen
def get_all_leaves(db: Session):
    return db.query(Leave).all()

# --- Gehaltsabrechnungsfunktionen ---
def add_payroll(db: Session, payroll: PayrollCreate):
    db_payroll = Payroll(
        employee_id=payroll.employee_id,
        salary=payroll.salary,
        payroll_date=payroll.payroll_date,
        deductions=payroll.deductions
    )
    db.add(db_payroll)
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def get_payroll_by_employee(db: Session, employee_id: int):
    return db.query(Payroll).filter(Payroll.employee_id == employee_id).all()

def update_payroll(db: Session, payroll_id: int, payroll: PayrollUpdate):
    db_payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    if db_payroll:
        db_payroll.salary = payroll.salary
        db_payroll.payroll_date = payroll.payroll_date
        db_payroll.deductions = payroll.deductions
        db.commit()
        db.refresh(db_payroll)
    return db_payroll

def delete_payroll(db: Session, payroll_id: int):
    db_payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    if db_payroll:
        db.delete(db_payroll)
        db.commit()
    return db_payroll

# ➕ NEU: Alle Gehaltsabrechnungen abrufen
def get_all_payrolls(db: Session):
    return db.query(Payroll).all()

# --- Benutzerfunktionen ---
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
