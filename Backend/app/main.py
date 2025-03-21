from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.endpoints.employees import router as employees_router
from app.api.endpoints.leave import router as leave_router
from app.api.endpoints.payroll import router as payroll_router
from app.api.endpoints.time_tracking import router as time_tracking_router
from app.db import session, repository
from app.schemas.user import User, UserCreate
from app.core.security import verify_password, create_access_token, get_password_hash, get_current_user  # Import hinzugefügt
from app.db.models import User as DBUser

# OAuth2PasswordBearer für Authentifizierung
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="TeamLink API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubt Anfragen nur von localhost:5173 (Frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Alle HTTP-Methoden erlauben (z.B. GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Alle Header erlauben
)

# Statische Dateien (z.B. für das Favicon) bereitstellen
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Favicon bereitstellen
@app.get("/favicon.ico")
def favicon():
    return FileResponse("app/static/favicon.ico")

# Endpoints einbinden
app.include_router(employees_router, prefix="/api/employees", tags=["employees"])
app.include_router(leave_router, prefix="/api/leave", tags=["leave"])
app.include_router(payroll_router, prefix="/api/payroll", tags=["payroll"])
app.include_router(time_tracking_router, prefix="/api/time_tracking", tags=["time_tracking"])

# Authentifizierungs-Endpunkt (Token generieren)
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(session.get_db)):
    # Benutzerdaten aus der DB basierend auf der E-Mail-Adresse
    user = repository.get_user_by_email(db, form_data.username)  # Hier muss `get_user_by_email` verwendet werden
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Überprüfen, ob das Passwort korrekt ist
    is_password_valid = verify_password(form_data.password, user.hashed_password)
    if not is_password_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generiere ein Access-Token für den Benutzer
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Benutzerregistrierung-Endpunkt (Optional)
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(session.get_db)):
    # Überprüfe, ob der Benutzer bereits existiert
    db_user = repository.get_user_by_email(db, user.email)  # Hier `get_user_by_email`
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash das Passwort des neuen Benutzers und speichere es als hashed_password
    user_password_hash = get_password_hash(user.password)
    
    new_user = DBUser(
        email=user.email, 
        hashed_password=user_password_hash  # Das gehashte Passwort speichern
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}

# Root-Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to TeamLink API!"}

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):  # Geänderte Funktion
    return {"message": "This is a protected route"}
