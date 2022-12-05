from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

PATH = "/api/v1/user"


# SIGNIN
def test_signin_user():
    response = client.post(PATH+"/signin", json={"email":"test@mail.com", "password":"123123"})
    assert response.status_code == 200
    return response.json()

def test_signin_admin():
    response = client.post(PATH+"/signin", json={"email":"admin@mail.com", "password":"123123"})
    assert response.status_code == 200
    return response.json()

def test_signin_fail():
    response = client.post(PATH+"/signin", json={"email":"test", "password":"test"})
    assert response.status_code == 400
    

# SIGNUP
def test_signup():
    response = client.post(PATH+"/signup", json={"name":"temp", "email":"temp@mail.com", "password":"123123"})
    assert response.status_code == 200

def test_signup_existing():
    response = client.post(PATH+"/signup", json={"name":"temp", "email":"temp@mail.com", "password":"123123"})
    assert response.status_code == 400


# PROFILE
def test_get_profile():
    user_token = test_signin_user()["access_token"]
    response = client.get(PATH+"/profile", headers={"Authorization": "Bearer "+user_token}, json={"id":1})
    assert response.status_code == 200
    return response.json()


# ALL
def test_get_all_users():
    admin_token = test_signin_admin()["access_token"]
    users = client.get(PATH+"/all", headers={"Authorization": f"Bearer {admin_token}"})
    assert users.status_code == 200
    return users.json()


# DELETE
def test_delete_user():
    admin_token = test_signin_admin()["access_token"]
    all_users = test_get_all_users()
    
    for x in all_users:
        if x["name"] == "temp":
            response = client.delete(PATH+"/delete", headers={"Authorization": f"Bearer {admin_token}"}, json={"id":x["id"]})
            assert response.status_code == 204