from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_recommendations():
    response = client.get("/recommendations/test_user")
    assert response.status_code == 200
