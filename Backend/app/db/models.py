from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hours_worked = Column(Integer, default=0)
