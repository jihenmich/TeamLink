from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.db.models import User
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.db import session  # Import hinzugefügt

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Konfiguration aus der .env-Datei holen
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  # Setze einen Standardwert für den Fall, dass die Umgebungsvariable fehlt
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Standard-Algorithmus
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Token läuft nach 30 Minuten ab

# Initialisiere den Passwort-Kontext für die Passwort-Hashing-Funktionen
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer für Authentifizierung
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Funktion zum Hashen des Passworts
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Funktion zur Überprüfung des Passworts
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Funktion zum Erstellen eines JWT Access Tokens
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Ablaufdatum des Tokens hinzufügen
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Funktion zum Abrufen eines Benutzers aus der Datenbank (basierend auf der E-Mail-Adresse)
def get_user(db: Session, email: str):  # Hier kannst du nach 'email' suchen, nicht nach 'username'
    return db.query(User).filter(User.email == email).first()  # Geändert von username zu email

# Funktion zur Überprüfung des Tokens und Abrufen des Benutzers
def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodiere das JWT-Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # E-Mail aus dem Payload extrahieren
        if email is None:
            raise credentials_exception
        return email  # Zurückgeben der E-Mail-Adresse des Benutzers
    except JWTError:
        raise credentials_exception

# Funktion zum Abrufen des aktuellen Benutzers aus dem Token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(session.get_db)):
    email = verify_token(token)
    print(f"Token valid for email: {email}")  # Debug-Ausgabe
    user = get_user(db, email=email)
    print(f"User found: {user}")  # Debug-Ausgabe
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
