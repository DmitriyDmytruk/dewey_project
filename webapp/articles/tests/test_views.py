from webapp.users.models import UserModel


def test_retrieve_articles(client, db):
    """
    Test articles retrieve api view (with decorators)
    :param client:
    :param db:
    :return:
    """
    response = client.get("/articles")
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    response = client.get(
        "/articles", headers={"Authorization": f"Token WrongToken"}
    )
    assert (
        response.json.get("message") == "Invalid token. Please log in again."
    )
    assert response.json.get("status") == 401

    user2 = (
        db.session.query(UserModel).filter_by(email="test2@gmail.com").one()
    )
    jwt_token = user2.encode_auth_token().decode("utf-8")
    response = client.get(
        "/articles", headers={"Authorization": f"Token {jwt_token}"}
    )
    assert response.json.get("message") == "Access denied."
    assert response.json.get("status") == 403

    user1 = db.session.query(UserModel).filter_by(email="test@gmail.com").one()
    jwt_token = user1.encode_auth_token().decode("utf-8")
    response = client.get(
        "/articles", headers={"Authorization": f"Token {jwt_token}"}
    )
    assert response.status_code == 200
