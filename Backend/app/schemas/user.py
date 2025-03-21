from pydantic import BaseModel, EmailStr

# Klasse für die Benutzererstellung (bei der Registrierung)
class UserCreate(BaseModel):
    email: EmailStr  # Ändere hier 'username' zu 'email', um es konsistent zu halten
    password: str  # Ungehashtes Passwort bei der Benutzererstellung

# Klasse für den Benutzer-Output (Daten, die beim Abrufen eines Benutzers verwendet werden)
class UserOut(BaseModel):
    id: int
    email: EmailStr  # 'email' statt 'username' verwenden

    class Config:
        orm_mode = True  # Damit Pydantic die Datenbankobjekte korrekt umwandeln kann

# Klasse für den Benutzer in der Datenbank (mit dem gehashten Passwort)
class UserInDB(UserOut):
    hashed_password: str  # Gehashtes Passwort in der DB

# Klasse für den Login (bei der Authentifizierung)
class Login(BaseModel):
    email: EmailStr  # Hier auch 'email' anstelle von 'username'
    password: str

# Hinzugefügte User-Klasse, die ein allgemeiner Benutzer-Datensatz sein könnte
class User(BaseModel):
    id: int
    email: EmailStr  # 'email' anstelle von 'username'

    class Config:
        orm_mode = True  # Damit Pydantic die Datenbankobjekte korrekt umwandeln kann
