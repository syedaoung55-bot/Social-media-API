from app import schems
from jose import jwt
from app.config import settings
import pytest

# Every test should be independent
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Welcome to my API here'
#     assert res.status_code == 200


def test_user_create(client):
    res = client.post("/users/", json={"email": "ali123@gmail.com", "password": "password123"})
    new_user = schems.UserOut(**res.json())
    assert new_user.email == "ali123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schems.token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@gmail.com', 'password123', 403),
    ('alim@gmail.com', 'wrongpassword', 403),
    ('wrong@gmail.com', 'password123', 403),
    (None, 'wrongpassword', 422),
    ('alim@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email , password, status_code):
    res = client.post("/login/", data={"username": email, "password": password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid credentials'