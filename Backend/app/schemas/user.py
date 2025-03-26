from pydantic import BaseModel, EmailStr

# Benutzerregistrierung (Input)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Benutzer-Daten als Output
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # Pydantic v2-kompatibel

# Benutzer-Daten aus DB (mit Passwort)
class UserInDB(UserOut):
    hashed_password: str

# Login-Daten (für OAuth2)
class Login(BaseModel):
    username: EmailStr  
    password: str

# Benutzer-Modell für interne Verwendung
class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
