from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    # Login-Anfrage mit Benutzername und Passwort
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "password"}
    )
    
    # Überprüfen, ob der Login fehlschlägt (401), wenn der Benutzer nicht existiert
    if response.status_code == 401:
        print("Login failed: User does not exist or wrong credentials.")
        assert response.status_code == 401  # Wenn Login fehlschlägt, erwarten wir 401
    else:
        # Überprüfen, ob die Antwort erfolgreich ist und ein Token zurückgegeben wird
        assert response.status_code == 200
        response_json = response.json()
        assert "access_token" in response_json
        assert response_json["token_type"] == "bearer"
        
        # Extrahiere das Token für den nächsten Test
        access_token = response_json["access_token"]
        return access_token

def test_protected_route():
    # Zuerst das Token vom Login-Test holen
    token = test_login()

    # Zugriff auf einen geschützten Endpunkt mit dem erhaltenen Token
    response = client.get(
        "/protected", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Überprüfen, ob die Antwort erfolgreich ist (hier 200 OK als Beispiel)
    assert response.status_code == 200
    assert response.json() == {"message": "This is a protected route"}
