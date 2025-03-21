# app/api/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db import session
from app.security import create_access_token, verify_password, get_user
from app.schemas.user import UserCreate, Login
from sqlalchemy.orm import Session
from app.db.models import User

router = APIRouter()

# OAuth2PasswordBearer gibt den Endpunkt zurück, wo der Token angefordert wird
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(session.get_db)):
    # Überprüfen, ob der Benutzer bereits existiert
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login_for_access_token(form_data: Login, db: Session = Depends(session.get_db)):
    user = get_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
