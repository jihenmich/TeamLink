# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

# Modell für Mitarbeiter
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hours_worked = Column(Integer, default=0)

    # Beziehungen zu den neuen Tabellen
    time_tracking = relationship("TimeTracking", back_populates="employee", cascade="all, delete-orphan")
    vacation_requests = relationship("VacationRequest", back_populates="employee", cascade="all, delete-orphan")
    payroll = relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")

# Modell für Zeiterfassung
class TimeTracking(Base):
    __tablename__ = "time_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))  # Beziehung zu Employee
    clock_in = Column(DateTime)
    clock_out = Column(DateTime)
    total_hours = Column(Integer)

    employee = relationship("Employee", back_populates="time_tracking")  # Rückbeziehung zu Employee

# Modell für Urlaubsanfragen
class VacationRequest(Base):
    __tablename__ = "vacation_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))  # Beziehung zu Employee
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default="Pending")  # Status der Anfrage: Pending, Approved, Rejected

    employee = relationship("Employee", back_populates="vacation_requests")  # Rückbeziehung zu Employee

# Modell für Gehaltsabrechnung
class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))  # Beziehung zu Employee
    salary = Column(Float)
    payroll_date = Column(Date)
    deductions = Column(Float, default=0.0)

    employee = relationship("Employee", back_populates="payroll")  # Rückbeziehung zu Employee
