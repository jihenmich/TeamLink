from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.time_tracking import TimeTrackingCreate, TimeTrackingUpdate
from app.db.models import TimeTracking

router = APIRouter()

#  Neue Zeiterfassung hinzufügen 
@router.post("/")
def add_time_tracking(time_tracking: TimeTrackingCreate, db: Session = Depends(session.get_db)):
    return repository.add_time_tracking(db=db, time_tracking=time_tracking)

#  Alle Zeiterfassungen abrufen
@router.get("/")
def get_all_time_tracking(db: Session = Depends(session.get_db)):
    return repository.get_all_time_tracking(db=db)

#  Zeiterfassungen eines Mitarbeiters
@router.get("/employee/{employee_id}")
def get_time_tracking_by_employee(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_time_tracking_by_employee(db=db, employee_id=employee_id)

#  Eintrag nach ID abrufen
@router.get("/{time_tracking_id}")
def get_time_tracking_by_id(time_tracking_id: int, db: Session = Depends(session.get_db)):
    return db.query(TimeTracking).filter(TimeTracking.id == time_tracking_id).first()

#  Zeiterfassung aktualisieren
@router.put("/{time_tracking_id}")
def update_time_tracking(time_tracking_id: int, time_tracking: TimeTrackingUpdate, db: Session = Depends(session.get_db)):
    return repository.update_time_tracking(db=db, time_tracking_id=time_tracking_id, time_tracking=time_tracking)

#  Zeiterfassung löschen 
@router.delete("/{time_tracking_id}")
def delete_time_tracking(time_tracking_id: int, db: Session = Depends(session.get_db)):
    return repository.delete_time_tracking(db=db, time_tracking_id=time_tracking_id)
