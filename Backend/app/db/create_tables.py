# create_tables.py

from app.db.session import Base, engine  
from app.db import models  


Base.metadata.create_all(bind=engine)

print("Tabellen wurden erfolgreich erstellt!")
