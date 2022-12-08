from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

USER_PATH = "/api/v1/user"
LIST_PATH = "/api/v1/list"

class TestList:

    @pytest.fixture
    def test_signin_user(self):
        response = client.post(USER_PATH+"/signin", json={"email":"test@mail.com", "password":"123123"})
        assert response.status_code == 200
        return response.json()

    def test_get_all_lists(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.get(LIST_PATH+"/user", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_get_joined_lists(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.get(LIST_PATH+"/joined", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        
    def test_get_active_lists(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.get(LIST_PATH+"/active", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_get_passive_lists(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.get(LIST_PATH+"/passive", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_get_public_lists(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.get(LIST_PATH+"/public", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_get_private_lists(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.get(LIST_PATH+"/private", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_create_list(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.post(LIST_PATH+"/create", headers={"Authorization": f"Bearer {user_token}"}, json={"name": "temp","items": [{"name": "temp","amount": 1,"bought_by": ""}],"is_active": True,"is_public": False})
        assert response.status_code == 200