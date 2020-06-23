import json

import flask_bcrypt

from webapp.users.models import UserModel


def test_non_registered_user_login(session, client):
    """ Test for login of user """
    password: str = "test_password"
    password_hash = flask_bcrypt.generate_password_hash(password).decode(
        "utf8"
    )
    user: UserModel = UserModel(
        email="patkennedy79@gmail.com",
        is_active=False,
        password=password_hash,
    )
    session.add(user)
    session.commit()

    # User does not exist, wrong email.
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(email="patkennedy79@gmail.com", password="123456")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["message"] == "User not found."
    assert response.content_type == "application/json"
    assert response.status_code == 404

    # Try again, login must be by email, not username
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(username="patkennedy78@gmail.com", password="123456")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["message"] == "Error. Try again"
    assert response.content_type == "application/json"
    assert response.status_code == 500

    # Fail, is_active == false
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(email="patkennedy79@gmail.com", password="test_password")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["message"] == "User not found."

    # Successful login
    user.is_active = True
    session.commit()
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(email="patkennedy79@gmail.com", password="test_password")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert "auth_token" in data
    assert data["message"] == "Successfully logged in."
    assert response.content_type == "application/json"
    assert response.status_code == 200


def test_user_create(session, client):
    """ Test for UserCreateAPI """
    password: str = "test_password"
    password_hash = flask_bcrypt.generate_password_hash(password).decode(
        "utf8"
    )
    user: UserModel = UserModel(
        email="patkennedy79@gmail.com",
        is_active=False,
        password=password_hash,
    )
    session.add(user)
    session.commit()

    # User does not exist, wrong email.
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(email="patkennedy79@gmail.com", password="123456")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["message"] == "User not found."
    assert response.content_type == "application/json"
    assert response.status_code == 404

    # Try again, login must be by email, not username
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(username="patkennedy78@gmail.com", password="123456")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["message"] == "Error. Try again"
    assert response.content_type == "application/json"
    assert response.status_code == 500

    # Fail, is_active == false
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(email="patkennedy79@gmail.com", password="test_password")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["message"] == "User not found."

    # Successful login
    user.is_active = True
    session.commit()
    response = client.post(
        "/users/login",
        data=json.dumps(
            dict(email="patkennedy79@gmail.com", password="test_password")
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert "auth_token" in data
    assert data["message"] == "Successfully logged in."
    assert response.content_type == "application/json"
    assert response.status_code == 200
