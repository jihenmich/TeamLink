# tests/test_endpoints.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_employee():
    # Mock-Daten für den Employee
    employee_data = {
        "name": "Jane Doe",
        "hours_worked": 120
    }

    response = client.post("/api/employees/", json=employee_data)

    # Testen, ob der Statuscode 200 OK ist
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"
    assert response.json()["hours_worked"] == 120
