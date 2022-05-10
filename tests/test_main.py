# project/tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_test_api():
    response = client.get("/api/v1/test_api")
    assert response.status_code == 200
    #assert response.json() == ["ok"]
