from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

USER_PATH = "/api/v1/user"

class TestUser:

    # SIGNIN
    @pytest.fixture
    def test_signin_user(self):
        response = client.post(USER_PATH+"/signin", json={"email":"test@mail.com", "password":"123123"})
        assert response.status_code == 200
        return response.json()

    def test_signin_fail(self):
        response = client.post(USER_PATH+"/signin", json={"email":"test", "password":"test"})
        assert response.status_code == 400
        

    # SIGNUP
    def test_signup(self):
        response = client.post(USER_PATH+"/signup", json={"name":"temp", "email":"temp@mail.com", "password":"123123"})
        assert response.status_code == 200

    def test_signup_existing(self):
        response = client.post(USER_PATH+"/signup", json={"name":"temp", "email":"temp@mail.com", "password":"123123"})
        assert response.status_code == 400


    # PROFILE
    def test_get_profile(self, test_signin_user):
        user_token = test_signin_user["access_token"]
        response = client.get(USER_PATH+"/profile", headers={"Authorization": "Bearer "+user_token}, json={"id":1})
        assert response.status_code == 200
        return response.json()