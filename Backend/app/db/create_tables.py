# create_tables.py

from app.db.session import Base, engine  # Base und engine importieren
from app.db import models  # Importiert die Models, damit sie im Schema berücksichtigt werden

try:
    # Alle Tabellen basierend auf den definierten Models erstellen
    Base.metadata.create_all(bind=engine)
    print("Tabellen wurden erfolgreich erstellt!")
except Exception as e:
    print(f"Fehler beim Erstellen der Tabellen: {e}")
