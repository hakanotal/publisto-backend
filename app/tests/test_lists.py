from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

PATH = "/api/v1/list"
TOKEN = client.post("/api/v1/user/signin", json={"email":"test@mail.com", "password":"123123"}).json()["access_token"]

class TestList:

    def test_get_all_lists(self):
        response = client.get(PATH+"/user", headers={"Authorization": f"Bearer {TOKEN}"})
        assert response.status_code == 200

    def test_get_joined_lists(self):
        response = client.get(PATH+"/joined", headers={"Authorization": f"Bearer {TOKEN}"})
        assert response.status_code == 200
        
    def test_get_active_lists(self):
        response = client.get(PATH+"/active", headers={"Authorization": f"Bearer {TOKEN}"})
        assert response.status_code == 200

    def test_get_passive_lists(self):
        response = client.get(PATH+"/passive", headers={"Authorization": f"Bearer {TOKEN}"})
        assert response.status_code == 200

    def test_get_public_lists(self):
        response = client.get(PATH+"/public", headers={"Authorization": f"Bearer {TOKEN}"})
        assert response.status_code == 200

    def test_get_private_lists(self):
        response = client.get(PATH+"/private", headers={"Authorization": f"Bearer {TOKEN}"})
        assert response.status_code == 200