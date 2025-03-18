from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Lade die Umgebungsvariablen
load_dotenv()

# Lade die Datenbank-URL aus der Umgebungsvariable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/teamlink")

# Erstelle die Engine
engine = create_engine(DATABASE_URL)

# SessionLocal für die Datenbankinteraktion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basis-Klasse für alle Models
Base = declarative_base()

# Funktion zur Bereitstellung der Datenbank-Sitzung
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Importiere deine Modelle
from app.db import models  # Modelle werden hier importiert, um sie zu registrieren und mit der Datenbank zu verbinden
