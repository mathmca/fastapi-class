import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post('/users/', json={"email": "hello123@gmail.com",
                                       "password": "pass123"})
    new_user = schemas.UserOut(**res.json())

    assert res.status_code == 201
    assert new_user.email == "hello123@gmail.com"


def test_login_user(client, test_user):
    res = client.post(
        '/login', data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, settings.algorithm)
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",
                         [
                             ('wrongemail@gmail.com', 'pass123', 403),
                             (None, 'password123', 422),
                             ('email@outlook.com', None, 422)
                         ])
def test_failed_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email,
                                      "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
