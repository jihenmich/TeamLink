# tests/test_oauth.py
import pytest
import requests
from unittest.mock import patch

# Beispiel API-Endpunkt
def get_oauth_token():
    response = requests.post("https://example.com/oauth", data={"client_id": "id", "client_secret": "secret"})
    return response.json()

# Testen mit Mocking des requests.post
def test_get_oauth_token(mocker):
    # Mock für die POST-Anfrage
    mock_response = mocker.patch("requests.post")
    mock_response.return_value.json.return_value = {"access_token": "mocked_token"}
    
    # Aufruf der Funktion
    token = get_oauth_token()

    # Testen, ob der Token korrekt zurückgegeben wird
    assert token["access_token"] == "mocked_token"
    mock_response.assert_called_once_with("https://example.com/oauth", data={"client_id": "id", "client_secret": "secret"})
