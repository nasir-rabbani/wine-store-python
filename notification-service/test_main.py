from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)


@patch("main.ses_client")
def test_send_notification(mock_ses_client):
    response = client.post(
        "/send-notification/",
        json={
            "email": "test@example.com",
            "subject": "Test",
            "message": "This is a test",
        },
    )
    assert response.status_code == 200
    mock_ses_client.send_email.assert_called_once()
