from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

# Modell für Mitarbeiter
class Employee(Base):
    __tablename__ = "employees"  # Der Tabellenname in der Datenbank

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hours_worked = Column(Integer, default=0)
    role = Column(String, default="")

    # Beziehungen zu den neuen Tabellen
    time_tracking = relationship("TimeTracking", back_populates="employee", cascade="all, delete-orphan")
    leave = relationship("Leave", back_populates="employee", cascade="all, delete-orphan")  # geändert von vacation_requests zu leave
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

# Modell für Urlaubsanfragen (jetzt als 'leave')
class Leave(Base):
    __tablename__ = "leave"  # Der Tabellenname ist nun 'leave'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))  # Beziehung zu Employee
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default="Pending")  # Status der Anfrage: Pending, Approved, Rejected

    employee = relationship("Employee", back_populates="leave")  # Rückbeziehung zu Employee (Geändert von vacation_requests zu leave)

# Modell für Gehaltsabrechnung
class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))  # Beziehung zu Employee
    salary = Column(Float)
    payroll_date = Column(Date)
    deductions = Column(Float, default=0.0)

    employee = relationship("Employee", back_populates="payroll")  # Rückbeziehung zu Employee


# Modell für Benutzer (OAuth-Authentifizierung)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Zum Speichern des gehashten Passworts
    
