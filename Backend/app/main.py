from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.endpoints.employees import router as employees_router
from app.api.endpoints.leave import router as leave_router
from app.api.endpoints.payroll import router as payroll_router
from app.api.endpoints.time_tracking import router as time_tracking_router
from app.api.endpoints.auth import router as auth_router

from app.db import session, repository
from app.schemas.user import UserCreate, User
from app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash,
    get_current_user
)
from app.db.models import User as DBUser

app = FastAPI(title="TeamLink API")

# CORS: Erlaube Zugriff vom Vite/React-Frontend
origins = [
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico")
def favicon():
    return FileResponse("app/static/favicon.ico")

# API-Router
app.include_router(employees_router, prefix="/api/employees", tags=["employees"])
app.include_router(leave_router, prefix="/api/leave", tags=["leave"])
app.include_router(payroll_router, prefix="/api/payroll", tags=["payroll"])
app.include_router(time_tracking_router, prefix="/api/time_tracking", tags=["time_tracking"])
app.include_router(auth_router, tags=["auth"])

# Token Endpoint (OAuth2)
@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(session.get_db)
):
    user = repository.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Registration Endpoint
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(session.get_db)):
    db_user = repository.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = DBUser(email=user.email, hashed_password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

# Root
@app.get("/")
def root():
    return {"message": "Welcome to TeamLink API!"}

# Protected Example Route
@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}
