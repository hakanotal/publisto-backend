from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_main_resource():
    response_auth = client.get("/")
    assert response_auth.status_code == 200