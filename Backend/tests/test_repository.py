# tests/test_repository.py
from app.db.repository import add_employee
from app.db.models import Employee
from app.schemas.employee import EmployeeCreate
import pytest
from unittest.mock import MagicMock

def test_add_employee(mocker):
    # Erstellen eines Mock-Objekts für die Session
    mock_db = MagicMock()

    # Eingabedaten für die EmployeeCreate
    employee_data = EmployeeCreate(name="John Doe", hours_worked=160)
    
    # Mock der commit() und refresh() Methoden der Session
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # Aufruf der zu testenden Funktion
    result = add_employee(mock_db, employee_data)

    # Überprüfen, ob die Methoden in der Session aufgerufen wurden
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    # Überprüfen, ob das Ergebnis ein Employee-Objekt ist
    assert isinstance(result, Employee)
    assert result.name == "John Doe"
    assert result.hours_worked == 160
