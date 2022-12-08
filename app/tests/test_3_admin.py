from fastapi.testclient import TestClient
import pytest

from ..main import app

client = TestClient(app)

USER_PATH = "/api/v1/user"
ADMIN_PATH = "/api/v1/admin"

class TestAdmin:

    # SIGNIN
    @pytest.fixture
    def test_signin_admin(self):
        response = client.post(f"{USER_PATH}/signin", json={"email":"admin@mail.com", "password":"123123"})
        assert response.status_code == 200
        return response.json()

    # USERS ALL
    @pytest.fixture
    def test_get_all_users(self, test_signin_admin):
        admin_token = test_signin_admin["access_token"]
        users = client.get(f"{ADMIN_PATH}/users/all", headers={"Authorization": f"Bearer {admin_token}"})
        assert users.status_code == 200
        return users.json()

    # USERS DELETE
    def test_delete_user(self, test_signin_admin, test_get_all_users):
        admin_token = test_signin_admin["access_token"]
        all_users = test_get_all_users
        
        for x in all_users:
            if x["name"] == "temp":
                response = client.delete(f"{ADMIN_PATH}/users/delete/{x['id']}", headers={"Authorization": f"Bearer {admin_token}"})
                assert response.status_code == 204

    # LISTS ALL
    @pytest.fixture
    def test_get_all_lists(self, test_signin_admin):
        admin_token = test_signin_admin["access_token"]
        lists = client.get(f"{ADMIN_PATH}/lists/all", headers={"Authorization": f"Bearer {admin_token}"})
        assert lists.status_code == 200
        return lists.json()

    # LISTS DELETE
    def test_delete_list(self, test_signin_admin, test_get_all_lists):
        admin_token = test_signin_admin["access_token"]
        all_lists = test_get_all_lists
        
        for x in all_lists:
            if x["name"] == "temp":
                response = client.delete(f"{ADMIN_PATH}/lists/delete/{x['id']}", headers={"Authorization": f"Bearer {admin_token}"})
                assert response.status_code == 204
