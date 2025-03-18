from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository, session
from app.schemas.time_tracking import TimeTrackingCreate
from app.db.models import TimeTracking  # Für Datenbankoperationen
from app.schemas.time_tracking import TimeTrackingUpdate

router = APIRouter()

# Zeiterfassung hinzufügen
@router.post("/{employee_id}/time-tracking/")
def add_time_tracking(employee_id: int, time_tracking: TimeTrackingCreate, db: Session = Depends(session.get_db)):
    time_tracking.employee_id = employee_id
    return repository.add_time_tracking(db=db, time_tracking=time_tracking)

# Zeiterfassung für einen Mitarbeiter abrufen
@router.get("/{employee_id}/time-tracking/")
def get_time_tracking(employee_id: int, db: Session = Depends(session.get_db)):
    return repository.get_time_tracking_by_employee(db=db, employee_id=employee_id)

# Zeiterfassung anhand der ID abrufen
@router.get("/time-tracking/{time_tracking_id}")
def get_time_tracking_by_id(time_tracking_id: int, db: Session = Depends(session.get_db)):
    return db.query(TimeTracking).filter(TimeTracking.id == time_tracking_id).first()

# Zeiterfassung aktualisieren
@router.put("/time-tracking/{time_tracking_id}")
def update_time_tracking(time_tracking_id: int, time_tracking: TimeTrackingUpdate, db: Session = Depends(session.get_db)):
    db_time_tracking = db.query(TimeTracking).filter(TimeTracking.id == time_tracking_id).first()
    if not db_time_tracking:
        return {"detail": f"Time tracking with ID {time_tracking_id} not found."}
    
    db_time_tracking.clock_in = time_tracking.clock_in
    db_time_tracking.clock_out = time_tracking.clock_out
    db_time_tracking.total_hours = time_tracking.total_hours
    db.commit()
    db.refresh(db_time_tracking)
    return db_time_tracking

# Zeiterfassung löschen
@router.delete("/time-tracking/{time_tracking_id}")
def delete_time_tracking(time_tracking_id: int, db: Session = Depends(session.get_db)):
    return repository.delete_time_tracking(db=db, time_tracking_id=time_tracking_id)
